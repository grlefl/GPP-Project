# GPP Project
- What frameworks are top publishers adopting? GPP? USP?
- Do publishers that have adopted the Global Privacy Platform (GPP) handle the Opt Out signal correctly?
- How is user preference handled differently across states? Which state privacy laws apply to a given publisher? 

## Timeline/Deadlines 
(incomplete)

## Task Overview

### Crawl 1 Tasks
  1. gather a csv file top publishers from Tranco (https://tranco-list.eu/)
     - narrow down list (only websites that load ??)
     - consider also adding domains of common data brokers (see methodology)

      <details>
        <summary>Methodology</summary><br>

        Johnny Still Can’t Opt-out: Assessing the IAB CCPA Compliance Framework
        
        > To gather data for this study, we chose to crawl the top 10 K domains from the Tranco list [36].7 We focus on the top 10 K domains because Van Nortwick and Wilson [60] found that the CCPA and CPRA were unlikely to apply to websites that fell below this level of popularity since they did not receive enough unique visitors from California to meet the laws’ eligibility criteria (see § 2.3). 

        > That said, the CCPA and CPRA may not apply to all domains in this list—e.g., domains owned by non-pro￿t organizations—and thus we refrain from asserting whether speci￿c websites are in compliance with the CCPA or CPRA (see § 3.5). Rather, the goal of our study is to assess the overall adoption of the CCPA Framework and ￿ows of consent information, a goal for which it is su￿cient for us to cover popular websites.

        Setting the Bar Low: Are Websites Complying With the Minimum Requirements of the CCPA?
     
        > To build our corpus, we joined the top 1 million domains from the research-oriented Tranco6 domain popularity ranking [60]...
        >
        > ... with 2,902 domains that were identified as third-party trackers and/or advertisers by Bashir et al. [15].7
        >
        > To further narrow this list, we performed an initial crawl in which we attempted to resolve each domain to a website, scrape its homepage, extract the page’s text, and then analyze the text with the Python langdetect library. Our crawler failed to retrieve a non-empty webpage from 267,718 (27%) of the domains in our initial list due to a variety of errors, including DNS resolution failure, connection failures, TLS errors, and HTTP 4XX and 5XX responses...
        > 
        >  Our final corpus of 497,870 domains includes those that successfully returned an HTML webpage containing English text.

      </details>

  2. establish a VPN
     - by default, use a California VPN to assess widespread adoption; focus on state-level analysis later
    
      <details>
        <summary>Methodology</summary><br>

        Johnny Still Can’t Opt-out: Assessing the IAB CCPA Compliance Framework

        Setting the Bar Low: Are Websites Complying With the Minimum Requirements of the CCPA?
     
        > All crawls were conducted using virtual machines from Amazon Web Services with IP addresses in California.
        
        > We assessed the impact of anti-crawler countermeasures on our crawler by manually revisiting 200 randomly selected websites, weighted by Tranco rank, from Crawl 3 and Crawl 4, using the same IP addresses as the crawler used.

      </details>

  4. determine which websites use GPP, USP
     - 

### Crawl 2 Tasks (is GPP being used correctly)
  1. step 1

### Crawl 3 Tasks (state-level analysis)
  1. step 1

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
