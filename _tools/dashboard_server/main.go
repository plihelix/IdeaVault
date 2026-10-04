package main

// Demo dashboard server.
//
// Tooling, not a note: no frontmatter, no ID, never cited as evidence (ADR-0015).
//
// It serves one page. The page asks the vault health service for its numbers
// itself, straight from the browser, so this server holds no state and runs no
// queries: it only hands out the three files next to it.
//
// Run: go run .
//      go build -o dashboard && ./dashboard

import (
	"context"
	"flag"
	"log"
	"net/http"
	"os"
	"os/signal"
	"path/filepath"
	"syscall"
	"time"
)

func main() {
	listen := flag.String("listen", "127.0.0.1:8081", "where the page is served")
	assets := flag.String("assets", "", "folder holding index.html (default: beside this program)")
	flag.Parse()

	root, err := resolveAssets(*assets)
	if err != nil {
		log.Fatalf("%v", err)
	}

	server := &http.Server{
		Addr:              *listen,
		Handler:           noStore(http.FileServer(http.Dir(root))),
		ReadHeaderTimeout: 10 * time.Second,
	}

	stop := make(chan os.Signal, 2)
	signal.Notify(stop, os.Interrupt, syscall.SIGTERM)
	go func() {
		if err := server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("listen: %v", err)
		}
	}()
	log.Printf("page       http://%s", *listen)
	log.Printf("files      %s", root)
	log.Printf("the page reads the vault health service directly; see its config.yaml")

	<-stop
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	if err := server.Shutdown(ctx); err != nil {
		log.Printf("shutdown: %v", err)
	}
}

// noStore keeps a refresh honest while the page is being looked at.
func noStore(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Cache-Control", "no-store")
		next.ServeHTTP(w, r)
	})
}

// resolveAssets finds the folder holding index.html: the given one, then the folder
// beside this program, then the current folder (go run builds elsewhere).
func resolveAssets(given string) (string, error) {
	candidates := []string{}
	if given != "" {
		candidates = append(candidates, given)
	}
	if exe, err := os.Executable(); err == nil {
		candidates = append(candidates, filepath.Dir(exe))
	}
	if cwd, err := os.Getwd(); err == nil {
		candidates = append(candidates, cwd)
	}
	for _, candidate := range candidates {
		if info, err := os.Stat(filepath.Join(candidate, "index.html")); err == nil && !info.IsDir() {
			return candidate, nil
		}
	}
	return "", &assetError{candidates}
}

type assetError struct {
	tried []string
}

func (e *assetError) Error() string {
	return "no index.html found in " + joinPaths(e.tried) + " (pass -assets)"
}

func joinPaths(paths []string) string {
	out := ""
	for index, path := range paths {
		if index > 0 {
			out += ", "
		}
		out += path
	}
	return out
}
