package main

// A reader for the YAML subset these config files use: nested mappings, lists of
// scalars or mappings, quoted or bare scalars, and comments. Anything richer
// (flow collections, block scalars, anchors, multiple documents) is refused with
// the offending line named, because a silently misread config is worse than none.

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Kind int

const (
	Scalar Kind = iota
	Mapping
	List
)

func (k Kind) String() string {
	switch k {
	case Mapping:
		return "mapping"
	case List:
		return "list"
	}
	return "scalar"
}

type Node struct {
	Kind   Kind
	Value  string
	Keys   []string
	Values map[string]*Node
	Items  []*Node
}

func newMapping() *Node { return &Node{Kind: Mapping, Values: map[string]*Node{}} }

func (n *Node) Get(key string) *Node {
	if n == nil || n.Kind != Mapping {
		return nil
	}
	return n.Values[key]
}

func (n *Node) Text() string {
	if n == nil || n.Kind != Scalar {
		return ""
	}
	return n.Value
}

func (n *Node) Bool(defaultValue bool) (bool, error) {
	if n == nil {
		return defaultValue, nil
	}
	if n.Kind != Scalar {
		return false, fmt.Errorf("expected true or false, found a %s", n.Kind)
	}
	switch strings.ToLower(n.Value) {
	case "true", "yes", "on":
		return true, nil
	case "false", "no", "off":
		return false, nil
	}
	return false, fmt.Errorf("expected true or false, found %q", n.Value)
}

func (n *Node) Int(defaultValue int) (int, error) {
	if n == nil || n.Value == "" {
		return defaultValue, nil
	}
	if n.Kind != Scalar {
		return 0, fmt.Errorf("expected a number, found a %s", n.Kind)
	}
	value, err := strconv.Atoi(n.Value)
	if err != nil {
		return 0, fmt.Errorf("expected a number, found %q", n.Value)
	}
	return value, nil
}

// Texts returns the strings of a list, or a single string, or nothing.
func (n *Node) Texts() []string {
	if n == nil {
		return nil
	}
	if n.Kind == List {
		out := make([]string, 0, len(n.Items))
		for _, item := range n.Items {
			out = append(out, item.Text())
		}
		return out
	}
	if n.Value == "" {
		return nil
	}
	return []string{n.Value}
}

type yamlLine struct {
	indent int
	text   string
	number int
}

func parseFile(path string) (*Node, error) {
	raw, err := os.ReadFile(path)
	if err != nil {
		return nil, err
	}
	return parseYAML(string(raw), path)
}

func parseYAML(text string, path string) (*Node, error) {
	var lines []yamlLine
	for index, raw := range strings.Split(text, "\n") {
		cleaned := strings.TrimRight(stripComment(raw), " \t\r")
		if cleaned == "" {
			continue
		}
		if strings.HasPrefix(cleaned, "---") || strings.HasPrefix(cleaned, "...") {
			return nil, fmt.Errorf("%s:%d: only one document per file is supported", path, index+1)
		}
		if strings.Contains(cleaned, "\t") {
			return nil, fmt.Errorf("%s:%d: indent with spaces, not tabs", path, index+1)
		}
		trimmed := strings.TrimLeft(cleaned, " ")
		lines = append(lines, yamlLine{
			indent: len(cleaned) - len(trimmed),
			text:   trimmed,
			number: index + 1,
		})
	}
	if len(lines) == 0 {
		return newMapping(), nil
	}
	node, used, err := parseBlock(lines, 0, lines[0].indent, path)
	if err != nil {
		return nil, err
	}
	if used != len(lines) {
		return nil, fmt.Errorf("%s:%d: unexpected indentation", path, lines[used].number)
	}
	return node, nil
}

// stripComment removes a comment that starts with # at the beginning of the line
// or after a space, leaving # inside quotes alone.
func stripComment(line string) string {
	var quote rune
	for i, r := range line {
		switch {
		case quote != 0:
			if r == quote {
				quote = 0
			}
		case r == '"' || r == '\'':
			quote = r
		case r == '#':
			if i == 0 || line[i-1] == ' ' || line[i-1] == '\t' {
				return line[:i]
			}
		}
	}
	return line
}

func parseBlock(lines []yamlLine, start, indent int, path string) (*Node, int, error) {
	if start >= len(lines) || lines[start].indent != indent {
		return nil, start, fmt.Errorf("%s: expected a line indented by %d spaces", path, indent)
	}
	if strings.HasPrefix(lines[start].text, "- ") || lines[start].text == "-" {
		return parseList(lines, start, indent, path)
	}
	return parseMapping(lines, start, indent, path)
}

func parseMapping(lines []yamlLine, start, indent int, path string) (*Node, int, error) {
	node := newMapping()
	i := start
	for i < len(lines) {
		current := lines[i]
		if current.indent < indent {
			break
		}
		if current.indent > indent {
			return nil, i, fmt.Errorf("%s:%d: unexpected indentation, expected %d spaces",
				path, current.number, indent)
		}
		if strings.HasPrefix(current.text, "- ") {
			break
		}
		key, rest, ok := splitKey(current.text)
		if !ok {
			return nil, i, fmt.Errorf("%s:%d: expected \"key: value\", found %q", path, current.number, current.text)
		}
		if _, seen := node.Values[key]; seen {
			return nil, i, fmt.Errorf("%s:%d: %s appears twice", path, current.number, key)
		}
		node.Keys = append(node.Keys, key)
		if rest != "" {
			switch {
			case strings.HasPrefix(rest, "{") || strings.HasPrefix(rest, "["):
				return nil, i, fmt.Errorf("%s:%d: write lists and maps over several lines", path, current.number)
			case rest == "|" || rest == ">" || strings.HasPrefix(rest, "|") || strings.HasPrefix(rest, ">"):
				return nil, i, fmt.Errorf("%s:%d: multi-line values are not supported", path, current.number)
			}
			node.Values[key] = &Node{Kind: Scalar, Value: unquote(rest)}
			i++
			continue
		}
		if i+1 < len(lines) && lines[i+1].indent > indent {
			child, used, err := parseBlock(lines, i+1, lines[i+1].indent, path)
			if err != nil {
				return nil, i, err
			}
			node.Values[key] = child
			i = used
			continue
		}
		node.Values[key] = &Node{Kind: Scalar, Value: ""}
		i++
	}
	return node, i, nil
}

func parseList(lines []yamlLine, start, indent int, path string) (*Node, int, error) {
	node := &Node{Kind: List}
	i := start
	for i < len(lines) {
		current := lines[i]
		if current.indent < indent {
			break
		}
		if current.indent > indent {
			return nil, i, fmt.Errorf("%s:%d: unexpected indentation, expected %d spaces",
				path, current.number, indent)
		}
		if !strings.HasPrefix(current.text, "- ") && current.text != "-" {
			break
		}
		rest := strings.TrimSpace(strings.TrimPrefix(current.text, "-"))
		if rest == "" {
			if i+1 < len(lines) && lines[i+1].indent > indent {
				child, used, err := parseBlock(lines, i+1, lines[i+1].indent, path)
				if err != nil {
					return nil, i, err
				}
				node.Items = append(node.Items, child)
				i = used
				continue
			}
			node.Items = append(node.Items, &Node{Kind: Scalar, Value: ""})
			i++
			continue
		}
		if strings.HasPrefix(rest, "{") || strings.HasPrefix(rest, "[") {
			return nil, i, fmt.Errorf("%s:%d: write lists and maps over several lines", path, current.number)
		}
		if _, _, isEntry := splitKey(rest); !isEntry {
			// A dash followed by a plain value: the item is that value.
			node.Items = append(node.Items, &Node{Kind: Scalar, Value: unquote(rest)})
			i++
			continue
		}
		// The dash line carries the first entry of a nested block, so the block
		// starts where the following lines actually line up.
		blockIndent := indent + 2
		if i+1 < len(lines) && lines[i+1].indent > indent {
			blockIndent = lines[i+1].indent
		}
		block := []yamlLine{{indent: blockIndent, text: rest, number: current.number}}
		j := i + 1
		for j < len(lines) && lines[j].indent > indent {
			block = append(block, lines[j])
			j++
		}
		child, used, err := parseBlock(block, 0, blockIndent, path)
		if err != nil {
			return nil, i, err
		}
		if used != len(block) {
			return nil, j, fmt.Errorf("%s:%d: unexpected indentation", path, block[used].number)
		}
		node.Items = append(node.Items, child)
		i = j
	}
	return node, i, nil
}

func splitKey(text string) (string, string, bool) {
	var quote rune
	for i, r := range text {
		if quote != 0 {
			if r == quote {
				quote = 0
			}
			continue
		}
		if r == '"' || r == '\'' {
			quote = r
			continue
		}
		if r != ':' {
			continue
		}
		rest := text[i+1:]
		if rest == "" || strings.HasPrefix(rest, " ") {
			return unquote(strings.TrimSpace(text[:i])), strings.TrimSpace(rest), true
		}
	}
	return "", "", false
}

func unquote(text string) string {
	if len(text) >= 2 {
		first, last := text[0], text[len(text)-1]
		if (first == '"' && last == '"') || (first == '\'' && last == '\'') {
			return text[1 : len(text)-1]
		}
	}
	return text
}
