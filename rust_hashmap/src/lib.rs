use pyo3::prelude::*;

#[pyclass(name = "Hashmap")]
pub struct HashMap {
    // Size is array index of key array
    pub size: usize,
    pub keys: [String; 1000],
    pub data: [String; 1000]
}

#[pymethods]
impl HashMap {

    #[new]
    pub fn new() -> Self {
        HashMap { size: 0, keys: [const {String::new()}; 1000], data: [const {String::new()}; 1000] }
    }

    fn hash(&self, key: String) -> usize {

        let mut hash: usize = 5381;

        for i in key.chars() {
            let c = i as usize;
            hash = ((hash << 5) + hash) + c; 
        }

        return hash % 1000;
    }

    pub fn insert(&mut self, key: String, value: String) {
        self.keys[self.size] = key.to_string();
        let arrayKey = self.hash(key.to_string());
        self.data[arrayKey] = value.to_string();
    }
    
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


/// A Python module implemented in Rust.
#[pymodule]
fn rust_hashmap(m: &Bound<'_, PyModule>) -> PyResult<()> {
    use pyo3::prelude::*;
    
    m.add_class::<HashMap>()?;
    Ok(())

}