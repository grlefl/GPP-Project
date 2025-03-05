# GPP Project
- What frameworks are top publishers adopting? GPP? USP?
- Do publishers that have adopted the Global Privacy Platform (GPP) handle the Opt Out signal correctly?
- How is user preference handled differently across states? Which state privacy laws apply to a given publisher? 

## Timeline/Deadlines 
(incomplete)

## Task Overview

### Crawl 1 Tasks - What compliance frameworks are top publishers using?
  1. gather a csv file top publishers from Tranco (https://tranco-list.eu/)
     - narrow down list (only websites that load ??)
     - consider also adding domains of common data brokers (see methodology)

      <details>
        <summary>Methodology</summary><br>

        Johnny Still Can’t Opt-out: Assessing the IAB CCPA Compliance Framework
        
        > To gather data for this study, we chose to crawl the top 10 K domains from the Tranco list [36].7 We focus on the top 10 K domains because Van Nortwick and Wilson [60] found          that the CCPA and CPRA were unlikely to apply to websites that fell below this level of popularity since they did not receive enough unique visitors from California to meet the         laws’ eligibility criteria (see § 2.3). 

        > That said, the CCPA and CPRA may not apply to all domains in this list—e.g., domains owned by non-pro￿t organizations—and thus we refrain from asserting whether speci￿c               websites are in compliance with the CCPA or CPRA (see § 3.5). Rather, the goal of our study is to assess the overall adoption of the CCPA Framework and ￿ows of consent                  information, a goal for which it is su￿cient for us to cover popular websites.

        Setting the Bar Low: Are Websites Complying With the Minimum Requirements of the CCPA?
     
        > To build our corpus, we joined the top 1 million domains from the research-oriented Tranco6 domain popularity ranking [60]...
        >
        > ... with 2,902 domains that were identified as third-party trackers and/or advertisers by Bashir et al. [15].7
        >
        > To further narrow this list, we performed an initial crawl in which we attempted to resolve each domain to a website, scrape its homepage, extract the page’s text, and then           analyze the text with the Python langdetect library. Our crawler failed to retrieve a non-empty webpage from 267,718 (27%) of the domains in our initial list due to a variety           of errors, including DNS resolution failure, connection failures, TLS errors, and HTTP 4XX and 5XX responses...
        > 
        >  Our final corpus of 497,870 domains includes those that successfully returned an HTML webpage containing English text.

      </details>

  2. establish a VPN
     - by default, use a California VPN to assess widespread adoption; focus on state-level analysis later
    
      <details>
        <summary>Methodology</summary><br>

        Setting the Bar Low: Are Websites Complying With the Minimum Requirements of the CCPA?
     
        > All crawls were conducted using virtual machines from Amazon Web Services with IP addresses in California.
        
        > We assessed the impact of anti-crawler countermeasures on our crawler by manually revisiting 200 randomly selected websites, weighted by Tranco rank, from Crawl 3 and Crawl           4, using the same IP addresses as the crawler used.

      </details>

  3. determine which websites use GPP/USP
     - preliminary work needed for general information (cookies, etc)
    
      <details>
        <summary>Preliminary Work Methodology</summary><br>

        Johnny Still Can’t Opt-out: Assessing the IAB CCPA Compliance Framework

        > We used custom scripts, written in Python and JavaScript, to drive and instrument an instance of Chrome8 using the Chrome DevTools Protocol [13]. We left Chrome at its               default settings, except during crawls where we varied HTTP headers, as described below.
        >
        > All crawls were conducted using virtual machines from Amazon Web Services with IP addresses in California.

        > During each crawl of the Tranco top 10 K, our crawler visited each domain one-by-one. For each domain, we programmed the crawler to load the domain’s homepage,9 scroll to the bottom of the page, then sleep for 25 seconds. Further, we programmed our crawler to select nine internal hyperlinks at random from the home-page and crawl them using the same load, scroll, and sleep approach.

        > We assessed the impact of anti-crawler countermeasures on our crawler by manually revisiting 200 randomly selected websites, weighted by Tranco rank, from Crawl 3 and Crawl 4, using the same IP addresses as the crawler used. We received CAPTCHA challenges on two of the websites that prevented them from loading normally. Thus, we estimate that around 1% of websites in our sample were impacted by anti-crawler countermeasures.
        
        > Our crawler recorded detailed
information during each visit to a webpage, including all HTTP
request and response headers and all cookies that were set. Fur-
thermore, our crawler recorded the resource inclusion tree for each
webpage [3, 6]... We decompose the inclusion tree for each webpage into
inclusion chains, where each chain corresponds to a unique path from root to leaf in the given tree [5]. Furthermore, given the focus
of our study, we isolated A&A chains that correspond to the serving
of an ad or a tracker. We label a given inclusion chain as an A&A
chain if (1) there was at least one HTTP request in the chain that
matched a rule in the EasyList or EasyPrivacy block lists,10 or (2)
the chain terminated in the loading of a 1⇥1 tracking pixel [21]. We
use these A&A chains in § 4 to analyze the sources and destinations
of HTTP requests that included the USP String, i.e., to understand
how this consent signal is being passed from one party to another.

      </details>

      <details>
        <summary>USP API Detection Methodology</summary><br>

        > Speci￿cally, the CCPA Framework requires that a
JavaScript method called __uspapi() be instantiated in the ￿rst-
party context. This method must support a getUSPData command
that returns a uspData object containing the USP String [31]. This
method can be called directly by third parties present in the ￿rst-
party context, or indirectly using the JavaScript postMessage DOM
API to communicate with a special __uspapiLocator iframe. The
CCPA Framework recommends that the USP String be stored in a
￿rst-party cookie named usprivacy and that it be shared using a
URL parameter with the name us_privacy. 

      </details>

      <details>
        <summary>GPP API Detection Methodology</summary><br>

      </details>

---

### Crawl 2 Tasks - Do publishers that have adopted GPP handle the Opt Out signal correctly?

Dependencies: A narrowed-down dataset from Crawl 1 is needed.  

  1. 

---

### Crawl 3 Tasks - How is user preference handled differently across states?

Dependencies: A narrowed-down dataset from Crawl 1 is needed.  

  1. 

---

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
