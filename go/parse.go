package main

// #cgo pkg-config: python3
// #include <python3.5m/Python.h>
// int PyArg_ParseTuple_S(PyObject * args, char** a);
// PyObject * Py_BuildValue_I(int a);
// PyObject * Py_BuildValue_F(float a);
import "C"
import (
	"bufio"
	"compress/gzip"
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
	currDate := line[dateIdx : dateIdx+17]

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

//export parse
func parse(self, args *C.PyObject) *C.PyObject {
	var path *C.char;
	ranges := make(map[string]*Range);

	if C.PyArg_ParseTuple_S(args, &path) == 0 {
		return nil;
    }

    parseFile(C.GoString(path), ranges)

    dict := C.PyDict_New();
	for k, r := range ranges {
		d := C.PyDict_New();
		C.PyDict_SetItemString(d, C.CString("upstream_count"), C.Py_BuildValue_I(C.int(r.upstreamCount)));
        C.PyDict_SetItemString(d, C.CString("static_count"), C.Py_BuildValue_I(C.int(r.staticCount)));
        C.PyDict_SetItemString(d, C.CString("err_count"), C.Py_BuildValue_I(C.int(r.errCount)));
        C.PyDict_SetItemString(d, C.CString("upstream_rt_sum"), C.Py_BuildValue_F(C.float(r.upstreamRtSum)));
        C.PyDict_SetItemString(d, C.CString("static_rt_sum"), C.Py_BuildValue_F(C.float(r.staticRtSum)));
        C.PyDict_SetItemString(d, C.CString("err_rt_sum"), C.Py_BuildValue_F(C.float(r.errRtSum)));
        C.PyDict_SetItemString(dict, C.CString(k), d);
	}

	return dict
}

func main() {}
