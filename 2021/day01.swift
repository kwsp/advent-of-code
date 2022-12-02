import Foundation

func getIntArray(_ fname: String) -> [Int] {
    do {
        let lines = try String(contentsOfFile: fname).split(separator: "\n")
        return lines.map({ Int($0) ?? -1 })
    } catch {
        print(error.localizedDescription)
    }
    return []
}

func countInc(_ arr: [Int]) -> Int {
    var count = 0
    var prev = arr[0]
    for v in arr[1...] {
        if prev < v {
            count += 1
        }
        prev = v
    }
    return count
}

func part1() {
    let arr = getIntArray("day01.txt")
    print(countInc(arr))
}

func part2() {
    let arr = getIntArray("day01.txt")
    var wind = Array(repeating: 0, count: arr.count-2)
    for i in 0..<arr.count-2 {
        wind[i] = arr[i] + arr[i+1] + arr[i+2]
    }
    print(countInc(wind))
}

part1()
part2()
