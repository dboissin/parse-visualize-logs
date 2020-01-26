extern crate flate2;
use std::collections::HashMap;
use std::fs::File;
use std::io::{self, prelude::*, BufReader};
use flate2::read::GzDecoder;

#[derive(Copy, Clone)]
struct Range {
    static_count: i32,
    upstream_count: i32,
    err_count: i32,
    static_rt_sum: f32,
    upstream_rt_sum: f32,
    err_rt_sum: f32
}

impl Range {

    fn new() -> Range {
        Range {
            static_count: 0,
            upstream_count: 0,
            err_count: 0,
            static_rt_sum: 0.0,
            upstream_rt_sum: 0.0,
            err_rt_sum: 0.0,
        }
    }

    fn update(&mut self, rt: f32, status: i32, empty_urt: bool) {
        if status > 399 {
            self.err_count += 1;
            self.err_rt_sum += rt;
        } else {
            if empty_urt {
                self.static_count += 1;
                self.static_rt_sum += rt
            } else {
                self.upstream_count += 1;
                self.upstream_rt_sum += rt
            }
        }
    }

}

fn parse_line(line: &str, ranges: &mut HashMap<String, Range>) -> Option<usize> {
    let date_idx:usize = line.find('[')? + 1;
    let rt_idx:usize = line.find("\"rt=")? + 4;
    let status_idx:usize = line.find("\" ")? + 2;

    let curr_date: String = line.chars().skip(date_idx).take(16).collect();

    if !ranges.contains_key(&curr_date) {
        ranges.insert(curr_date.to_owned(), Range::new());
    }
    let range = ranges.get_mut(&curr_date)?;

    let rt: f32 = line.chars().skip(rt_idx).take(5).collect::<String>().parse::<f32>().ok()?;
    let status: i32 = line.chars().skip(status_idx).take(3).collect::<String>().parse::<i32>().ok()?;

    let empty_urt = match line.find("urt=\"-") {
        Some(_) => true,
        None => false,
    };

    range.update(rt, status, empty_urt);

    Some(0)
}

fn parse_file(path: &str, ranges: &mut HashMap<String, Range>) -> io::Result<()> {
    let mut line = String::with_capacity(4096);
    let mut reader = BufReader::new(File::open(path)?);

    loop {
        line.clear();
        let r = reader.read_line(&mut line);
        if r.is_err() || r? == 0 {
            break;
        }
        parse_line(&line, ranges);
    }

    Ok(())
}

fn parse_gz_file(path: &str, ranges: &mut HashMap<String, Range>) -> io::Result<()> {
    let mut line = String::with_capacity(4096);
    let mut reader = BufReader::new(GzDecoder::new(File::open(path)?));

    loop {
        line.clear();
        let r = reader.read_line(&mut line);
        if r.is_err() || r? == 0 {
            break;
        }
        parse_line(&line, ranges);
    }

    Ok(())
}

fn main() {
    let mut ranges: HashMap<String, Range> = HashMap::new();
    let path = "../../logs/access.log.gz";
    if path.ends_with(".gz") {
        parse_gz_file(path, &mut ranges);
    } else {
        parse_file(path, &mut ranges);
    }
    for (k, v) in &ranges {
        println!("{},{},{},{},{},{},{}", k, v.upstream_count, v.upstream_rt_sum,
                v.static_count, v.static_rt_sum, v.err_count, v.err_rt_sum);
    }
}

