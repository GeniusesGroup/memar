/* For license and copyright information please see the LEGAL file in the code repository */

package utm_p

// Urchin Tracking Module (UTM) parameters
// https://en.wikipedia.org/wiki/UTM_parameters
type MarketingUTM interface {
	Source() string   // Identifies which site sent the traffic, and is a required parameter.		"utm_source=google.com", "Referer: <url>"
	Medium() string   // Identifies what type of link was used, such as cost per click or email.	utm_medium=cpc
	Campaign() string // Identifies a specific product promotion or strategic campaign.				utm_campaign=spring_sale
	Term() string     // Identifies search terms.													utm_term=running+shoes
	Content() string  // Identifies what specifically was clicked to bring the user to the site.	utm_content=logolink or utm_content=textlink	such as a banner ad or a text link. It is often used for A/B testing and content-targeted ads.
}
