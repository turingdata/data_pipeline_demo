## Overview
Our goal is to build production-ready software that is _reliable_, _scalable_ and _maintainable_.

__Reliability__
* The system should continue to work correctly (performing the correct function at the desired performance) even in the face of adversity (hardware or software faults, and even human error).

__Scalability__
* As the system grows (in data volume, traffic volume or complexity), there should be reasonable ways of dealing with that growth.

__Maintainability__
* Over time, many different people will work on the system (engineering and operations, both maintaining current behavior and adapting the system to new use cases), and they should all be able to work on it productively.

We build production-ready software by embracing continuous delivery and building quality into products as our highest priority. [Kent Beck](https://www.kentbeck.com) came up with [four simple rules of design](http://martinfowler.com/bliki/BeckDesignRules.html) in the late 1990's that we apply to every line of code we write:

 * Passes the tests
 * Reveals intention
 * No duplication
 * Fewest elements

## Four Simple Rules of Design
### Passes the tests
Test driving code is the most important rule. As stated by Beck:

> ... whatever else you do with the software, the primary aim is that it works as intended, and tests are there to ensure that happens.

To achieve this, we use BDD (Behavior-Driven Development, also know as TDD - Test-Driven Development). The following is a description of BDD from Noel Rappin's book __[Master Space and Time with Javascript](http://www.noelrappin.com/)__:

> In the BDD process, you write a test that describes a logical change to your program, which could be a new feature or a bug you are looking to squash. You then write the code that makes that test pass. The general process looks like this:
> - Write a specification for a small change to your program.
> - Write the simplest code that makes that test pass.
> - Refine the code by cleaning it up, removing any duplication added, and improving the implementation, a process known as refactoring. This step is important. In a BDD system, this is where much of your design takes place.

> Repeat until done. The process is often referred to as "Red/Green/Refactor", since most test runners use red to indicate test failure and green to indicate test passage.

This provides four primary benefits:

- controls code bloat
- keeps test coverage high making future refactoring fear-free and easy
- typically yields better design by keeping classes small and decoupled
- provides documentation of exactly what a system does

Simply put, tests communicate to the team (including your future-self) exactly what the code does. [Jay Fields](http://blog.jayfields.com) put it best:

> Any fool can write a test that helps them today. Good programmers write tests that help the entire team in the future.

If you have not worked in an environment that test drives code, please watch the following videos:
- [RailsCast - How I Test](http://railscasts.com/episodes/275-how-i-test)
- [Jim Weirich's __Roman Numerals Kata__](https://www.youtube.com/watch?v=983zk0eqYLY&t=314) _(skips first 5 minutes)_
- [Corey Haines' __Fast Rails Tests__](http://www.youtube.com/watch?v=bNn6M2vqxHE)

### Reveals intention
Code should be easy to understand. It should express its intentions to other team members, and your future self, of what your purpose was when writing it. If you feel like you need to add comments to your code to explain it, you're doing something wrong. The manual side of the code review helps quickly identify and fix code that is not intention-revealing.

### No duplication
This is often referred to as the [DRY (Don't Repeat Yourself) principle](http://en.wikipedia.org/wiki/Don't_repeat_yourself) and was originally coined by [Dave Thomas](http://en.wikipedia.org/wiki/Dave_Thomas_(programmer)) and [Andy Hunt](http://en.wikipedia.org/wiki/Andy_Hunt_(author)) in __[The Pragmatic Programmer](https://pragprog.com/book/tpp/the-pragmatic-programmer)__. The idea here is that...

> ... every piece of knowledge must have a single, unambiguous, authoritative representation within a system.

When the DRY principle is applied successfully, a modification of any single element of a system does not require a change in other logically unrelated elements. Keeping code DRY is much harder than it sounds and typically requires a tool such as [flay](https://github.com/seattlerb/flay) or [codeclimate](http://codeclimate.com) to help identify and correct issues, and this is where the automated side of our code review comes into play.

### Fewest elements
Any code that doesn't serve the three prior rules should be removed, which brings us to the concept of [YAGNI (You Ain't Gonna Need It)](http://en.wikipedia.org/wiki/You_aren't_gonna_need_it). [Ron Jeffries](http://en.wikipedia.org/wiki/Ron_Jeffries) put this as:

> Always implement things when you actually need them, never when you just foresee that you need them.

This rule is harder than it sounds. We are all experienced programmers and tend draw on our past experiences and failures. The business has a backlog of future features we might do, so why not lay the ground work for that in my current feature branch?

Because the only guarantee in business and software is change, and thinking you can know the future is the best way to bloat a codebase with dead code. [Sandi Metz](http://www.sandimetz.com/) [puts this best](http://www.amazon.com/Practical-Object-Oriented-Design-Ruby-Addison-Wesley/dp/0321721330/):

> The future is uncertain and you will never know less than you know right now.

If we embrace this ethos and stick firmly to rule #1, we can keep both technical debt and code-bloat to a minimum.
