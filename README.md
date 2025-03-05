# GPP Project
- What frameworks are top publishers adopting? GPP? USP?
- Do publishers that have adopted the Global Privacy Platform (GPP) handle the Opt Out signal correctly?
- How is user preference handled differently across states? Which state privacy laws apply to a given publisher? 

## Timeline/Deadlines 
(incomplete)

## Task Overview

### Crawl 1 Tasks
  1. develop a list of top websites from Tranco (https://tranco-list.eu/)
     - narrow down list (only websites that load)
     - consider also adding domains of common data brokers (see methodology) 

  3. establish a VPN
     - For now, I think the default California VPN is fine. Don't want to worry about state-level analysis in this crawl. 

  4. determine which websites use GPP, USP
     - 

### Crawl 2 Tasks
  1. check if GPP being handled correctly

### Crawl 3 Tasks 
  1. state-level analysis 

### Extra Compliance Analysis 

## Possible Tools to Use
(incomplete)(copy over from Project Proposal)

## Extra Resources/References 

https://github.com/InteractiveAdvertisingBureau/Global-Privacy-Platform/blob/main/Core/Consent%20String%20Specification.md
- Digital property owners or CMPs are responsible for generating, persisting, and passing the GPP String.
- strings encoded with Fibonacci

https://github.com/InteractiveAdvertisingBureau/Global-Privacy-Platform/blob/main/Core/CMP%20API%20Specification.md

Notes
- pull websites from top ## from Tranco (bigger or lesser depending on user counts for other analysis)
- check if companies use GPP in the first place
- then we make our own version of the CMP API to instantiate before website loads and see the stack trace of what websites access it ??

- get Semrush data, but this is a separate component that can be done whenever 
