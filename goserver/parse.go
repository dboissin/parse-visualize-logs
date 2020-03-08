package main

import (
	"bufio"
	"compress/gzip"
	"encoding/json"
	"log"
	"net/http"
	"os"
	"strconv"
	"strings"
)

type Range struct {
	Datetime string `json:"datetime"`
	Prefix string `json:"prefix"`
	StaticCount   int32 `json:"static_count"`
	UpstreamCount int32 `json:"upstream_count"`
	ErrCount      int32 `json:"err_count"`
	StaticRtSum   float64 `json:"static_rt_sum"`
	UpstreamRtSum float64 `json:"upstream_rt_sum"`
	ErrRtSum      float64 `json:"err_rt_sum"`
}

func parseLine(line string, ranges map[string]*Range) {
	var prefix string
	dateIdx := strings.Index(line, "[") + 1
	rtIdx := strings.Index(line, "\"rt=") + 4
	statusIdx := strings.Index(line, "\" ") + 2
	prefixIdx := strings.Index(line, " /") + 2
	endUriIdx := strings.Index(line, " HTTP/")

	currDate := line[dateIdx : dateIdx+17]
	if prefixIdx > 1 && endUriIdx > 0 {
		uri := line[prefixIdx:endUriIdx]
		endPrefixIdx := strings.Index(uri, "/")
		if endPrefixIdx > 0 {
			prefix = uri[0:endPrefixIdx]
		} else {
			prefix = "/"
		}
	} else {
		prefix = "/"
	}

	var r = ranges[currDate + prefix]
	if r == nil {
		r = &(Range{currDate, prefix, 0, 0, 0, 0.0, 0.0, 0.0})
		ranges[currDate + prefix] = r
	}

	rt, err := strconv.ParseFloat(line[rtIdx:rtIdx+5], 64)
	if err != nil {
		log.Fatal("parse float error")
	}
	status, err2 := strconv.ParseInt(line[statusIdx:statusIdx+3], 10, 32)
	if err2 != nil {
		log.Fatal("parse int error")
	}

	if status > 399 {
		r.ErrCount += 1
		r.ErrRtSum += rt
	} else {
		urtIdx := strings.Index(line, "urt=\"-")
		if urtIdx > 0 {
			r.StaticCount += 1
			r.StaticRtSum += rt
		} else {
			r.UpstreamCount += 1
			r.UpstreamRtSum += rt
		}
	}
}

func parseFile(path string, ranges map[string]*Range) {
	file, err := os.Open(path)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	var scanner *bufio.Scanner
	if strings.HasSuffix(path, ".gz") {
		gz, err := gzip.NewReader(file)
		if err != nil {
			log.Fatal(err)
		}
		scanner = bufio.NewScanner(gz)
		defer gz.Close()
	} else {
		scanner = bufio.NewScanner(file)
	}

	for scanner.Scan() {
		parseLine(scanner.Text(), ranges)
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
}

func parseHandler(w http.ResponseWriter, r *http.Request) {
	ranges := make(map[string]*Range);

	parseFile("../logs/access.log", ranges)
	values := []*Range{}
    for _, value := range ranges {
        values = append(values, value)
    }
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(values)
}

func main() {
	http.HandleFunc("/parse", parseHandler)
	http.ListenAndServe(":9081", nil)
}
