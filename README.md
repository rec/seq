# seq: A very generic little Python sequencer

...as simple as possible but no simpler...

The basics.
--

There are just three basic concepts: _Time_,  _Context_ and _Executable_.

A _Time_ is exactly what you think of it as: a relative ("in ten minutes") or
absolute ("midnight EST January 1 2000") time.

A _Context_ is a dictionary of variable assignments - of name=value pairs.

You can think of a Context as "the state of the world at a given time".  For
example, in the case of a motor system, the Context would contain all the motors
and information about, say, buttons and sensors.

In an old-style program, this "Context" would have just been global variables.
We however want to be able to have multiple sequences running on "different
worlds" at once, so we pull out all the "mutable global state" as computer
scientists would say, and call it a Context.

And an _Executable_ is nothing more than a Python function that operates on a
Context!

That's it - the sequencer just calls an _Executable_ and gives it a _Context_
and it "does something" - what that "something" is depends entirely on your
project.

A _Sequence_ is just a collection of Executables and Times, and all the
sequencer does is "play" Executables at different times!

Why is this interesting?
--

If you're a handy Python programmer, writing a sketch at a sequencer might take
you a few minutes, so why is this interesting?

First, writing a bullet-proof sequencer that gracefully starts up and shuts down
turns out to be non-trivial, though reasonably straight-forward.

But there are also subtleties that will (hopefully) make this easy, pleasant
and powerful to use.

_Persistance_:

You can recall and store your sequences on disk.

_Editable_

Sequences are in clear, human-readable [JSON](http::/json.org).  The format is
flexible: there are many ways to enter sequences, and most intuitive ways of
"just typing it in" will work.

_Extensible_

You can easily and seamlessly reference `seq` code, your own code, and code from
external libraries in the same sequence.

_Packaging_

In a later revision of this program, I plan to meld it in with another project
of mine, one which (is supposed to) allow you to register Python code (in an
optional [virtualenv](https://virtualenv.readthedocs.org/en/latest/) to be run
at startup.

That would mean that you could write your program using `seq`, then type a
single command and have it run at startup (automatically handling things like
"turning off blanking and screen savers", etc).

Examples of `seq` data.
--

My aim is to be as "dumb" as possible - within the confines of what JSON will
allow of course.

If you have a "dumb", "obvious" way to represent a sequence of events and I'm
not covering it, let me know and I'll try to figure out a way to cover it.

Let's suppose that your project is called `motor`, and you have code in
`motor.py` that looks like:

    def run(context):
        context.giant_robot.crush('Minneapolis')
        context.audio.cackle_madly()

A. `"motor.run"`

This single string (with quotes) is a valid sequence.  It means, "Immediately
call the function `motor.run(context)`."

B. `[2.0, "motor.run"]`

This list with two elements means, "Wait two seconds, then call
`motor.run(context)`.

Here are other ways of saying the same thing:

    {2.0: "motor.run"}
    [[2.0, "motor.run"]]
    [{2.0: "motor.run"}]

C. `{2.0: "motor.run", 2.5: "motor.stop"}`

This dictionary means, "At time 2.0 seconds, call `motor.run(context)`; at
time 2.5 seconds, call `motor.stop(context)`.

D. `{2.0: ["motor.run", [0.5: "motor.stop"]}`

This dictionary means, "At time 2.0 seconds, call `motor.run(context)`, then
wait 0.5 more seconds, and call `motor.stop(context)` - which has the same
effect as the other one!

It can't stay quite this simple for long - so what if there's an option speed
parameter to `motor.run` - so it looks like `def run(context, speed=10): ...` -
and you want to run at half-speed?

E. `[2.0, "motor.run", {"speed": 5}]`

That wasn't so bad, was it?

What if you want to do more than one thing?

F. `[2.0, ["motor.run", "duck.quack", "blender.chop"]]`

(This is another spin on the idea in D.)

G. `{"a": "motor.run", "b": "ball.spin", "c": "blender.chop"}`

What's this?  No times at all?

This is a _jump table_ and you will use that for real-time triggering of
events - in this case, you might be assigning these commands to the computer
keyboard.


FAQ
--

A. If this is so flexible, won't it be ambiguous?

There's a fairly straight-forward grammar underneath it that should make it
deterministic.  I think you'd have to work pretty hard to write something
ambiguous, and the result would be an error message, not "silently doing the
wrong thing".


B. There are further facilities I need for my project.

I'm trying to keep the scope of this as narrow as possible - though there will
be further facilities for e.g. starting and stopping sequences from other
sequences or from external triggers.

Because executables can come from _any_ Python package that you have installed
on your machine, the possibilities are endless to write your own code.

#
