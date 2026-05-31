use core::num;

pub struct HashMap<const u: usize> {
    pub size: usize,
    pub table: [String; u],
}


impl<const u: usize> HashMap<u> {
    // Constructor convention
    pub fn new() -> HashMap<u> {
        HashMap { size: u, table: [const {String::new()}; u] }
    }

    // Read-only method (borrows self)
    pub fn print(&self) {
        println!("Starting!");
        for i in self.table.iter() {
            println!("{i}");
        }
    }
}

fn main() {
    println!("Hello, world!");
    let hash:HashMap<20000> = HashMap::new();
    hash.print();
}
