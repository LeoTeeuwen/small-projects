use pyo3::prelude::*;

#[pyclass(name = "Hashmap")]
pub struct HashMap {
    // Size is array index of key array
    pub size: usize,
    // For clean printing
    pub keys: [String; 1000],
    // Both key and data pair stored in data array, (key, data) is the protocol
    pub data: [(String, String); 1000]
}


#[pymethods]
impl HashMap {
    // Constructor convention
    #[new]
    pub fn new() -> Self {
        HashMap { size: 0, keys: [const {String::new()}; 1000], data: [const {((String::new(), String::new()))}; 1000] }
    }

    fn hash(&self, key: String) -> usize {

        let mut hash: usize = 5381;

        for i in key.chars() {
            let c = i as usize;
            hash = ((hash << 5) + hash) + c; 
        }

        let val = hash % 1000;
        return hash % 1000;
    }

    // Make sure to normalize output to size of array! (1000)
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
            arrayKey = (arrayKey + arrayKey2) % 1000;
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
                arrayKey = (arrayKey + arrayKey2) % 1000;
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


/// A Python module implemented in Rust.
#[pymodule]
fn rust_hashmap(m: &Bound<'_, PyModule>) -> PyResult<()> {
    use pyo3::prelude::*;
    
    m.add_class::<HashMap>()?;
    Ok(())

}