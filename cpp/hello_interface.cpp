#include <iostream>

///////////////////////////////////////////////////////////////////////////////
// Nothing in the rulebook says you can't have more than one interface
// referencing the same virtual function. We'll often we want to narrow a
// consumer to make it easier to implement a contract.
//
// As far as SOLID goes this corresponds to the Interface Segregation Principle
// (ISP), or the "I" of SOLID. The advantage of narrowing these interfaces is
// that we can partially implement variants of BigService and still have them
// remain compatible with some (but not necessarily all) consumers.
//
// In this example we could easily reimplement LaunchRocket() and have it
// remain compatible with RocketMan via the IElonMusk interface. If RocketMan
// were to consume BigService directly it would unnecessarily end up with
// parts of the other contracts and would most likely throw NotImplemented
// exceptions. Doing this will violate Liskov Substitution Principle (LSP).
///////////////////////////////////////////////////////////////////////////////

// Define a bunch of contracts.

class IBritish {
public:
	virtual ~IBritish() {}
	virtual void EatFishAndChips() = 0;
	virtual void AddSalt() = 0;
	virtual void AddVinegar() = 0;
	virtual void MakeTea() = 0;
};

class IThirsty {
public:
	virtual ~IThirsty() {}
	virtual void MakeTea() {}
	virtual void BrewCoffee() = 0;
};

class IElonMusk {
public:
	virtual ~IElonMusk() {}
	virtual void LaunchRocket() = 0;
};

///////////////////////////////////////////////////////////////////////////////
// BigService would probably be some large object in the system acting as glue
// to other services. The most obvious example would be a logging adapter
// which might log these operations to a production log server. The goal of
// this object is to wrap all the contract functionality around its
// implementation - usually for lifetime control.
///////////////////////////////////////////////////////////////////////////////

class BigService : public IBritish, public IThirsty, public IElonMusk {
public:
	virtual ~BigService() {}
	virtual void MakeTea() { std::cout << "Making Tea." << std::endl; }
	virtual void BrewCoffee() { std::cout << "Brewing Coffee." << std::endl; }
	virtual void HostYardSale() { std::cout << "Hosting Yard Sale." << std::endl; }
	virtual void LaunchRocket() { std::cout << "Launching Rocket." << std::endl; }
	virtual void AddSugar() { std::cout << "Adding Sugar." << std::endl; }
	virtual void EatFishAndChips() { std::cout << "Eating Fish & Chips." << std::endl; }
	virtual void AddSalt() { std::cout << "Adding Salt." << std::endl; }
	virtual void AddVinegar() { std::cout << "Adding Vinegar." << std::endl; }
};

///////////////////////////////////////////////////////////////////////////////
// The actual working objects are here. Due to the interfaces it's fairly easy
// to determine the scope of access to BigService. The compiler won't let you
// call functionality on BigService that's outside your contract.
///////////////////////////////////////////////////////////////////////////////

class IDoThings {
public:
	virtual ~IDoThings() {}
	virtual void DoThings() = 0;
};

// Concrete types.

class BadBritishPerson : public IDoThings {
protected:
	// You would never want to consume this object directly as BigService
	// doesn't actually define a contract. If BigService were connected to
	// a logging system or database this could easily cause massive
	// dependencies to leak into what should be a trivial object.
	BigService& _service;
public:
	BadBritishPerson(BigService& service) : _service(service) {}
	void DoThings() override {
		std::cout << "** BadBritishPerson Doing Things..." << std::endl;
		_service.LaunchRocket();
		_service.HostYardSale();
	}
};

class GoodBritishPerson : public IDoThings {
protected:
	IBritish& _service;
public:
	GoodBritishPerson(IBritish& service) : _service(service) {}
	void DoThings() override {
		std::cout << "** GoodBritishPerson Doing Things..." << std::endl;
		// _service.LaunchRocket(); // Doesn't work
		_service.EatFishAndChips();
		_service.AddSalt();
		_service.AddVinegar();
		_service.MakeTea();
	}
};

class ThirstyPerson : public IDoThings {
protected:
	IThirsty& _service;
public:
	ThirstyPerson(IThirsty& service) : _service(service) {}
	void DoThings() override {
		std::cout << "** ThirstyPerson Doing Things..." << std::endl;
		// _service.EatFishAndChips(); // Doesn't work
		_service.MakeTea();
		_service.BrewCoffee();
	}
};

class RocketMan : public IDoThings {
protected:
	IElonMusk& _service;
public:
	RocketMan(IElonMusk& service) : _service(service) {}
	void DoThings() override {
		std::cout << "** RocketMan Doing Things..." << std::endl;
		// _service.MakeTea(); // Doesn't work
		_service.LaunchRocket();
	}
};

int main(int argc, char** argv) {
	BigService service;
	BadBritishPerson brit1(service);
	GoodBritishPerson brit2(service);
	ThirstyPerson brit3(service);
	RocketMan notbrit(service);	

	std::vector<IDoThings*> people = { &brit1, &brit2, &brit3, &notbrit };
	for (auto& brit : people) {
		brit->DoThings();
	}
	return 0;
}
