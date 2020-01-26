package main

import (
	"bufio"
	"compress/gzip"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

type Range struct {
	staticCount   int32
	upstreamCount int32
	errCount      int32
	staticRtSum   float64
	upstreamRtSum float64
	errRtSum      float64
}

func parseLine(line string, ranges map[string]*Range) {
	dateIdx := strings.Index(line, "[") + 1
	rtIdx := strings.Index(line, "\"rt=") + 4
	statusIdx := strings.Index(line, "\" ") + 2
	currDate := line[dateIdx : dateIdx+16]

	var r = ranges[currDate]
	if r == nil {
		r = &(Range{0, 0, 0, 0.0, 0.0, 0.0})
		ranges[currDate] = r
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
		r.errCount += 1
		r.errRtSum += rt
	} else {
		urtIdx := strings.Index(line, "urt=\"-")
		if urtIdx > 0 {
			r.staticCount += 1
			r.staticRtSum += rt
		} else {
			r.upstreamCount += 1
			r.upstreamRtSum += rt
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

func main() {
	ranges := make(map[string]*Range)
	parseFile("../logs/access.log.gz", ranges)
	for k, r := range ranges {
		fmt.Printf("%s,%d,%f,%d,%f,%d,%f\n",
			k, r.upstreamCount, r.upstreamRtSum,
			r.staticCount, r.staticRtSum, r.errCount,
			r.errRtSum)
	}
}
