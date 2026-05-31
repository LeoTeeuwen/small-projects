use core::num;
use std::iter;

pub struct HashMap<const u: usize> {
    pub size: usize,
    pub table: [String; u],
    // TODO implement a new data pair attribute here
}


impl<const u: usize> HashMap<u> {
    // Constructor convention
    pub fn new() -> HashMap<u> {
        HashMap { size: u, table: [const {String::new()}; u] }
    }

    fn hash(&self, key: String) -> usize {

        let mut hash: usize = 5381;

        for i in key.chars() {
            let c = i as usize;
            hash = ((hash << 5) + hash) + c; 
        }

        return hash % self.size;
    }

    // TODO fix for data pair
    pub fn insert(&mut self, key: &String) {
        let arrayKey = self.hash(key.to_string());
        self.table[arrayKey] = key.to_string();
    }

    // TODO fix for data pair
    pub fn search(&self, key: String) -> String {
        let arrayKey = self.hash(key);
        return self.table[arrayKey].clone();
    }

    pub fn print(&self) {
        println!("Starting!");
        for i in self.table.iter() {
            println!("{i}");
        }
    }
}

fn main() {
    println!("Hello, world!");
    let mut hash:HashMap<20000> = HashMap::new();
    hash.insert(&("Hello!".to_string()));
    let found = hash.search("Hello!".to_string());

    println!("{found}")
    
}
