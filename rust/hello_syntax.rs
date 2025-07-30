fn main() {
	test_mutable();
	test_integer();
	test_float();
	test_bool();
	test_char();
	test_tuple();
	test_branch();
}

////////////////////////////////////////
// Mutable Variables
fn test_mutable() {
	let x = 3;
	println!("x = {x}");
	//y = 6; // Error: Immutable
	let mut y = 4;
	println!("y = {y}");
	y = 5;
	println!("y = {y}");
}

////////////////////////////////////////
// Integer Types
fn test_integer() {
	let vari8: i8 = 127;
	//let vari8ovf: i8 = 128; // Error: Overflow
	println!("i8 = {vari8}");
	let vari16: i16 = 32767;
	//let vari16ovf: i16 = 32768; // Error: Overflow
	println!("i16 = {vari16}");
	let vari32: i32 = 2000000000;
	println!("i32 = {vari32}");
	let vari64: i64 = 2000000000;
	println!("i64 = {vari64}");
	let vari128: i128 = 2000000000;
	println!("i128 = {vari128}");
	let varu8: u8 = 255;
	println!("u8 = {varu8}");
	let varu16: u16 = 65535;
	println!("u16 = {varu16}");
	let varu32: u32 = 4000000000;
	println!("u32 = {varu32}");
	let varu64: u64 = 4000000000;
	println!("u64 = {varu64}");
	let varu128: u128 = 4000000000;
	println!("u128 = {varu128}");
}

////////////////////////////////////////
// Floating Point Types
fn test_float() {
	let varf32: f32 = 123.45;
	println!("f32 = {varf32}");
	let varf64: f64 = 123.456789;
	println!("f64 = {varf64}");
}

////////////////////////////////////////
// Boolean Types
fn test_bool() {
	let varbool: bool = false;
	println!("bool = {varbool}");
}

////////////////////////////////////////
// Char Types
fn test_char() {
	let varchar: char = '😎';
	println!("char = {varchar}");
}

////////////////////////////////////////
// Tuple Types
fn test_tuple() {
	let vartuple: (u32, u16, f32) = (4000000000, 65535, 123.456);
	//println!("(u32, u16, f32 = {vartuple}"); // Error: Unsupported
	let vare0 = vartuple.0;
	let vare1 = vartuple.1;
	let vare2 = vartuple.2;
	println!("tup.0 = {vare0}");
	println!("tup.1 = {vare1}");
	println!("tup.2 = {vare2}");
}

////////////////////////////////////////
// Branches
fn test_branch() {
	let x = 5;
	if x < 5 {
		println!("(1) This is not executed.");
	} else {
		println!("(1) This is executed.");
	}
	if x > 3 {
		println!("(2) This is executed.");
	} else {
		println!("(2) This is not executed.");
	}
	let varbool: bool = false;
	if !varbool {
		println!("(3) This is executed.")
	}
}