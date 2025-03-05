# GPP Project
- What frameworks are top publishers adopting? GPP? USP?
- Do publishers that have adopted the Global Privacy Platform (GPP) handle the Opt Out signal correctly?
- How is user preference handled differently across states? Which state privacy laws apply to a given publisher? 

## Timeline/Deadlines 
(incomplete)

## Task Overview

### Crawl 1 Tasks
  1. develop a list of top websites from Tranco (https://tranco-list.eu/)
     - narrow down list (only websites that load ??)
     - consider also adding domains of common data brokers (see methodology)

      <details>
        <summary>Methodology</summary><br>

        Johnny Still Can’t Opt-out: Assessing the IAB CCPA Compliance Framework
        
        > To gather data for this study, we chose to crawl the top 10 K domains from the Tranco list [36].7 We focus on the top 10 K domains because Van Nortwick and Wilson [60] found that the CCPA and CPRA were unlikely to apply to websites that fell below this level of popularity since they did not receive enough unique visitors from California to meet the laws’ eligibility criteria (see § 2.3). 

        > That said, the CCPA and CPRA may not apply to all domains in this list—e.g., domains owned by non-pro￿t organizations—and thus we refrain from asserting whether speci￿c websites are in compliance with the CCPA or CPRA (see § 3.5). Rather, the goal of our study is to assess the overall adoption of the CCPA Framework and ￿ows of consent information, a goal for which it is su￿cient for us to cover popular websites.

      </details>

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
