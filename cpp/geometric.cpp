///////////////////////////////////////////////////////////////////////////////
// Classic Streaming Interfaces.
///////////////////////////////////////////////////////////////////////////////

class IStreamIn {
public:
	virtual ~IStreamIn() {}
	virtual void ReadBytes(void* buffer, int count) = 0;
};

class IStreamOut {
public:
	virtual ~IStreamOut() {}
	virtual void WriteBytes(const void* buffer, int count) = 0;
};

class ISerializable {
public:
	virtual ~ISerializable() {}
	virtual void Load(IStreamIn& stream) = 0;
	virtual void Save(IStreamOut& stream) = 0;
};

///////////////////////////////////////////////////////////////////////////////
// Output Stream Implementors.
//
// Streaming interfaces are common and can be overridden to perform all kinds
// of interesting behaviors. The obvious use is to provide streaming outputs to
// network sockets, files, or memory buffers - this also makes them Adaptors in
// design pattern parlance.
///////////////////////////////////////////////////////////////////////////////

#include <iostream>

class Log : public IStreamOut {
public:
	Log() {
		std::cout << "[Opening Log]" << std::endl;
	}
	virtual ~Log() {
		std::cout << std::endl << "[Closing Log]" << std::endl;
	}
	virtual void WriteBytes(const void* buffer, int count) {
		for (int i = 0; i < count; ++i) {
			std::cout << " " << ((const uint8_t*)buffer)[i];
		}
	}
};

#include <ctime>

class LogTime : public IStreamOut {
public:
	LogTime() {
		std::cout << "[Opening Timestamped Log]" << std::endl;
	}
	virtual ~LogTime() {
		std::cout << "[Closing Timestamped Log]" << std::endl;
	}
	virtual void WriteBytes(const void* buffer, int count) {
		time_t t;
		time(&t);
		std::cout << "[" << t << "]";
		for (int i = 0; i < count; ++i) {
			std::cout << " " << ((const uint8_t*)buffer)[i];
		}
		std::cout << std::endl;
	}
};

class MemoryStream : public IStreamOut {
protected:
	std::vector<uint8_t> _memory;
public:
	virtual void WriteBytes(const void* buffer, int count) {
		for (int i = 0; i < count; ++i) {
			_memory.push_back(((const uint8_t*)buffer)[i]);
		}
	}
	uint32_t size() const {
		return _memory.size();
	}
};

///////////////////////////////////////////////////////////////////////////////
// Standard Geometrics.
//
// This is a rudimentary world setup intended only to demonstrate a usage of
// concepts.
///////////////////////////////////////////////////////////////////////////////

#include <exception>

class NotImplementedException : public std::exception {
};

// Tagging Interface
// Doesn't do anything except declare an object.

class IObject {
public:
	virtual ~IObject() {}
};

class Box : public IObject, public ISerializable {
protected:
	float _x, _y, _z;
public:
	Box(float x, float y, float z) : _x(x), _y(y), _z(z) {}
	virtual void Load(IStreamIn& stream) override {
		throw NotImplementedException();
	}
	virtual void Save(IStreamOut& stream) override {
		stream.WriteBytes("Box", 3);
		stream.WriteBytes(&_x, sizeof(_x));
		stream.WriteBytes(&_y, sizeof(_y));
		stream.WriteBytes(&_z, sizeof(_z));
	}
};

class Sphere : public IObject, public ISerializable {
protected:
	float _radius;
public:
	Sphere(float radius) : _radius(radius) {}
	virtual void Load(IStreamIn& stream) override {
		throw NotImplementedException();
	}
	virtual void Save(IStreamOut& stream) override {
		stream.WriteBytes("Sphere", 6);
		stream.WriteBytes(&_radius, sizeof(_radius));
	}
};

class Mesh : public IObject, public ISerializable {
protected:
	int _vertices, _triangles;
public:
	Mesh(int vertices, int triangles) : _vertices(vertices), _triangles(triangles) {
	}
	virtual void Load(IStreamIn& stream) override {
		throw NotImplementedException();
	}
	virtual void Save(IStreamOut& stream) override {
		stream.WriteBytes("Mesh", 4);
		stream.WriteBytes(&_vertices, sizeof(_vertices));
		stream.WriteBytes(&_triangles, sizeof(_triangles));
	}
};

///////////////////////////////////////////////////////////////////////////////
// Geometric Factory.
//
// We use a factory pattern to create the world either as parametric/geometric
// objects or as mesh data. This is a basic example of an abstract factory.
///////////////////////////////////////////////////////////////////////////////

class ISceneFactory {
public:
	virtual ~ISceneFactory() {}
	virtual std::unique_ptr<IObject> CreateBox(float x, float y, float z) = 0;
	virtual std::unique_ptr<IObject> CreateSphere(float radius) = 0;
};

// Geometrics are parametric objects that cannot be directly renderered
// (except via raytracers) as they are not b-reps.
class GeomFactory : public ISceneFactory {
public:
	virtual std::unique_ptr<IObject> CreateBox(float x, float y, float z) override {
		return std::make_unique<Box>(x, y, z);
	}
	virtual std::unique_ptr<IObject> CreateSphere(float radius) override {
		return std::make_unique<Sphere>(radius);
	}
};

// The MeshFactory is a stand-in for mesh data but it doesn't actually
// create any triangle meshes (yet).
class MeshFactory : public ISceneFactory {
public:
	virtual std::unique_ptr<IObject> CreateBox(float x, float y, float z) override {
		return std::make_unique<Mesh>(8, 12);
	}
	virtual std::unique_ptr<IObject> CreateSphere(float radius) override {
		return std::make_unique<Mesh>(36 * 36, 36 * 36 * 2);
	}
};

//////////////////////////////////////////////////////////////////////////////
// Command Pattern.
//
// This is a very naive implementation of a command pattern that supports undo
// (as long as the commands are maintained in a second list).
//////////////////////////////////////////////////////////////////////////////

class ICommand {
public:
	virtual ~ICommand() {}
	virtual void CommandDo() = 0;
	virtual void CommandUndo() = 0;
};

///////////////////////////////////////////////////////////////////////////////
// Entrypoint.
///////////////////////////////////////////////////////////////////////////////

// Simple strategy to save everything in the world.
// This corresponds to a visitor pattern.

template <class T> using Array = std::vector<T>;

using SharedFactory = std::shared_ptr<ISceneFactory>;

using SharedObject = std::shared_ptr<IObject>;
using World = Array<SharedObject>;
using SharedWorld = std::shared_ptr<World>;

using SharedCommand = std::shared_ptr<ICommand>;
using Commands = Array<SharedCommand>;
using SharedCommands = std::shared_ptr<Commands>;

///////////////////////////////////////////////////////////////////////////////
// This is a command pattern.
///////////////////////////////////////////////////////////////////////////////

class CreateBoxCommand : public ICommand {
protected:
	SharedWorld _world;
	float _x, _y, _z;
	SharedFactory _factory;
public:
	CreateBoxCommand(SharedWorld& world, float x, float y, float z) : _world(world), _x(x), _y(y), _z(z) {}
	virtual void CommandDo() override {
		_world->push_back(std::move(_factory->CreateBox(_x, _y, _z)));
	}
	virtual void CommandUndo() override {
		_world->pop_back();
	}
};

class CreateSphereCommand : public ICommand {
protected:
	SharedWorld _world;
	float _radius;
	SharedFactory _factory;
public:
	CreateSphereCommand(SharedWorld& world, float radius) : _world(world), _radius(radius) {}
	virtual void CommandDo() override {
		_world->push_back(std::move(_factory->CreateSphere(_radius)));
	}
	virtual void CommandUndo() override {
		_world->pop_back();
	}
};

SharedWorld CreateWorld(ISceneFactory& factory) {
	std::cout << "Creating World..." << std::endl;
	SharedWorld world = std::make_shared<World>();
	world->push_back(std::move(factory.CreateBox(2.0f, 3.0f, 4.0f)));
	world->push_back(std::move(factory.CreateSphere(1.0f)));
	world->push_back(std::move(factory.CreateSphere(2.0f)));
	return world;
}

// Visitor pattern - walk through the objects of the world and call
// a function on each one.
void VisitObjects(SharedWorld& world, std::function<void(IObject&)> fn) {
	for (auto& i : *world) {
		fn(*i.get());
	}
}

void SaveEverything(SharedWorld& world, IStreamOut& stream) {
	std::cout << "Serializing objects..." << std::endl;
	// Using the visitor pattern to serialize objects.
	// Serialization is a relatively simple case of marching through
	// objects and calling their serialization methods.
	VisitObjects(world, [&stream](IObject& obj) {
		ISerializable* serial = dynamic_cast<ISerializable*>(&obj);
		if (serial != nullptr) {
			serial->Save(stream);			
		}
	});
}

// Save the "world" to different stream out implementors.
void SaveMethods(SharedWorld& world) {
	{
		Log log;
		SaveEverything(world, log);
	}
	{
		LogTime log;
		SaveEverything(world, log);
	}
	{
		MemoryStream str;
		SaveEverything(world, str);
		std::cout << "Buffer contains " << str.size() << " bytes." << std::endl;
	}
}


// Main Entrypoint.

int main(int argc, const char** argv) {
	{
		std::cout << "** Using Geometry Factory" << std::endl;
		GeomFactory factory;
		SharedWorld world = CreateWorld(factory);
		SaveMethods(world);
	}
	{
		std::cout << "** Using Mesh Factory" << std::endl;
		MeshFactory factory;
		SharedWorld world = CreateWorld(factory);
		SaveMethods(world);
	}
	return 0;
}