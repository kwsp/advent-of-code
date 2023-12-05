import Foundation

func getInput(_ fname: String) -> [(String, Int)] {
    do {
        let lines = try String(contentsOfFile: fname).split(separator: "\n")
        return lines.map{line in 
            let pair = line.split(separator: " ")
            return (String(pair[0]), Int(pair[1]) ?? Int())
        }
    } catch {
        print(error.localizedDescription)
    }
    return []
}

func part2() {
    let inp = getInput("day02.txt")
    var hor = 0, depth = 0, aim = 0
    inp.forEach{(d, v) in 
        switch d {
        case "forward":
            hor += v
            depth += aim * v
        case "down":
            aim += v
        case "up":
            aim -= v
        default:
            break
        }
    }
    print(hor * depth)
}

func part1() {
    let inp = getInput("day02.txt")
    var hor = 0, depth = 0
    inp.forEach{(d, v) in 
        switch d {
        case "forward":
            hor += v
        case "down":
            depth += v
        case "up":
            depth -= v
        default:
            break
        }
    }
    print(hor * depth)
}

part1()
part2()
