pub struct HashMap<const u: usize> {
    // Size is array index of key array
    pub size: usize,
    pub keys: [String; u],
    pub data: [String; u]
}


impl<const u: usize> HashMap<u> {
    // Constructor convention
    pub fn new() -> HashMap<u> {
        HashMap { size: 0, keys: [const {String::new()}; u], data: [const {String::new()}; u] }
    }

    fn hash(&self, key: String) -> usize {

        let mut hash: usize = 5381;

        for i in key.chars() {
            let c = i as usize;
            hash = ((hash << 5) + hash) + c; 
        }

        return hash % u;
    }

    // TODO fix for data pair
    pub fn insert(&mut self, key: &String, value: &String) {
        self.keys[self.size] = key.to_string();
        let arrayKey = self.hash(key.to_string());
        self.data[arrayKey] = value.to_string();
    }
    
    // TODO fix for data pair
    pub fn search(&self, key: String) -> String {
        let arrayKey = self.hash(key.to_string());
        return self.data[arrayKey].clone();
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
    println!("Hello, world!");
    let mut hash:HashMap<10000> = HashMap::new();
    hash.insert(&"Hello".to_string(), &"World".to_string());
    let found = hash.search("Hello".to_string());    
}
