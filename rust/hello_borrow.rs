fn main() {
	let mut int: i32 = 123;
	let ptr = &mut int;
	println!("{int}"); // Error: mutable reference of int in scope
	*ptr = 456;
}