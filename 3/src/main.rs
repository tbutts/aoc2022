// lol but i dont kno rust tho??!?!?!??!?!

use std::collections::HashSet;

// const alpha_l: &str = "abcdefghijklmnopqrstuvwxyz";
// const alpha_u: &str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
const PRIORITY_RANGE: &str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";

fn part1(puzzle: &str) -> usize {
    // Sample input line: vJrwpWtwJgWrhcsFMMfFFhFp
    let sacks: Vec<[HashSet<char>; 2]> = puzzle
        .split_whitespace()
        .filter(|s| s.len() > 1)
        .map(|s| {
            let (l,r) = s
                .split_at(s.len()/2);

            [l,r].map(|s| s.chars().collect::<HashSet<char>>())
        })
        .collect();

    let mismatches: Vec<&char> = sacks
        .iter()
        .map(|[l,r]|
            l.intersection(&r).next().unwrap())
        .collect();

    mismatches
        .into_iter()
        .map(|ch| PRIORITY_RANGE.find(*ch).unwrap() + 1 )
        .sum()
}

type Sack = HashSet<char>;

fn part2(puzzle: &str) -> usize {
    puzzle
        .split_whitespace()
        .filter(|s| s.len() > 1)
        // the worst impl of core::iter::Iterator::array_chunks (nightly experimental) you could imagine
        //   nevermind! jfc, a vector of vectors inside a closure is a nightmare.
        //      I bet I could get gpt3 to solve this for me but man what the hell
        //        oh wtf, I can convert to a vector THEN call chunks, but array_chunks is experimental
/*         .fold(vec![vec![]], |mut acc: Vec<Vec<&str>>, s| {
            let end = acc.last().unwrap();
            if end.len() >= 3 {
                acc.push(vec![s])
            } else {
                end.push(s)
            }
            acc
        });
 */
        .collect::<Vec<_>>()
        .chunks(3)
        // no breaks on this functional method call train, woo woooooo 🚞
        .map(|tri|
            tri.into_iter()
                .fold(
                    PRIORITY_RANGE.chars().collect::<Sack>(),
                    |acc, s| s.chars().collect::<Sack>().intersection(&acc.clone()).map(|c| c.to_owned()).collect()
                )
                .iter()
                .next()
                .unwrap()
                .clone() // incredibly heavy operation to get a single utf8 codepoint
        )
        .map(|ch| PRIORITY_RANGE.find(ch).unwrap() + 1)
        .sum()

}


#[cfg(test)]
mod tests {
    use super::*;

    static TEST: &str = " \
#vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw";

    // what in the god damn why does this test fail 4/5 of the time?
    // there's barely anything going on? why is it random?
    // why is the wrong answer always off by 2? (159)
    // what is going on?
    #[test]
    fn example_1() {
        let expect = 159;
        assert_eq!(part1(&TEST), expect);
    }

    #[test]
    fn example_2() {
        let expect = 70;
        assert_eq!(part2(&TEST), expect);
    }
}

fn main() {
    let input = include_str!("../input.txt");
    println!("{}", part1(input));
    println!("{}", part2(input));
}
