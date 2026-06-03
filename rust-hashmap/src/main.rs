use std::process::exit;

pub struct HashMap<const u: usize> {
    // Size is array index of key array
    pub size: usize,
    // For clean printing
    pub keys: [String; u],
    // Both key and data pair stored in data array, (key, data) is the protocol
    pub data: [(String, String); u]
}


impl<const u: usize> HashMap<u> {
    // Constructor convention
    pub fn new() -> HashMap<u> {
        HashMap { size: 0, keys: [const {String::new()}; u], data: [const {((String::new(), String::new()))}; u] }
    }

    fn hash(&self, key: String) -> usize {

        let mut hash: usize = 5381;

        for i in key.chars() {
            let c = i as usize;
            hash = ((hash << 5) + hash) + c; 
        }

        let val = hash % u;
        return hash % u;
    }

    // Make sure to normalize output to size of array! (u)
    fn hash2(&self, key: String) -> usize {
        let PRIME = 10903;
        let mut hash: usize = 10903;

        for i in key.chars() {
            let c = i as usize;
            hash = ((hash << 5) + hash) + c; 
        }
        return PRIME - (hash%PRIME);
    }

    pub fn insert(&mut self, key: String, value: String) {
        self.keys[self.size] = key.to_string();

        let mut arrayKey: usize = self.hash(key.to_string());
        let arrayKey2: usize = self.hash2(key.to_string());

        while(self.data[arrayKey].1 != "") {
            arrayKey = (arrayKey + arrayKey2) % u;
        }

        self.data[arrayKey].0 = key.to_string();
        self.data[arrayKey].1 = value.to_string();
        self.size += 1;
    }
    
    pub fn search(&self, key: String) -> String {
        let mut arrayKey: usize = self.hash(key.to_string());
        let arrayKey2: usize = self.hash2(key.to_string());

        loop {
            if (self.data[arrayKey].1 == "") {
                break;
            } else if (self.data[arrayKey].0 == key.to_string())  {
                return (self.data[arrayKey].1).to_string();
            } else if (self.data[arrayKey].0 != key.to_string()) {
                arrayKey = (arrayKey + arrayKey2) % u;
            }
        }

        return "Not in array!".to_string();
    }

    pub fn print(&self) {
        println!("Starting!");
        for i in self.keys.iter() {
            if i != "" {
                println!("{i}");
            }
        }
    }
}

fn main() {
    let mut hash:HashMap<5000> = HashMap::new();
    
    hash.insert("HfKlo".to_string(), "World1!".to_string());
    let mut found = hash.search("HfKlo".to_string());    
    println!("{found}");
    
    hash.insert("HemKo".to_string(), "World2!".to_string());
    found = hash.search("HemKo".to_string());    
    println!("{found}");
    
    found = hash.search("Hello".to_string());    
    println!("{found}");
}
