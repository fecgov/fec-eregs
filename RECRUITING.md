# Recruiting Staff

Scratching out some notes for recruiting devs/designers.

## What is eRegs

* Goal: make regulations easier to understand
* Parser
    * converts semi-structured regulation into a more usable form
    * uses that information to create versions of the regulation over time
    * derives extra value from the reg - citations, definitions, etc.
    * finds/processes external info, analyses, etc.
* UI
    * Navigable, searchable interface to that data
    * Clean, clear design
    * Mobile friendly
    * Somewhat skinnable
* Stack
    * Parser is Python, with many, many libraries
    * API and UI backend are Django
    * Frontend is Backbone + Less

## Agencies

* CFPB originated the project, has a team devoted to maintaining it for their
  regs. It currently holds two of their regs, but will shortly hold more
* ATF has an instance which 18F maintains. Currently holds one reg, though
  this will also be expanded shortly
* FEC liked a demo Micah put together a lot, hired their own devs to work on
  getting their regulation in. We provide some support, but may expand this
  role
* Other agencies are interested, but aren't spun up

## Short-term future

* Import more regulations and spread to more agencies. This means tweaking our
  data structures, etc. to accommodate and manually inspecting results. This
  applies to CFPB, ATF, and FEC
* Focus on maintainability. We currently require more or less an entire team
  to handle updates to regulations
* Notice and Comment. This is a substantial new module (or even application)
  that would provide a nice interface for tracking how regulations are
  expected to change and allowing comments to be made on these changes
* New features. Each agency will have different focuses of interest and
  desired functionality.

## What do we need

We need multiple folks with overlapping skillsets. Some of the skillsets the
project as a whole needs:

* Architecture - there are lots of moving parts here
* Data structures/algorithms - we aren't afraid of leveraging comp sci
* XML processing - most of our input is XML
* Natural Language Processing - we don't dive super deep here now (mostly
  relying on heuristics and keywords), but this would be a growth area
* Python (or Ruby, Lua, other scripting languages)
* LESS - particularly around skinning the application for additional agencies,
  but also for Notice and Comment and other new features
* Javascript - particularly for Notice and Comment and potentially for other
  new features
* Design - particularly for Notice and Comment and potentially for new other
  new features
