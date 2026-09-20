package ztna

import "fmt"

// ContextGraph represents an instance of resource access. It includes detailed information
// about the access request such as the targeted resource, the agent requesting access,
// the mode of access, the client application used, the issuer of the request,
// and additional attributes like the creator, owner, and verifiable credentials.
type ContextGraph struct {
	Target           string
	Agent            string
	Mode             string
	Client           string
	Issuer           string
	Creator          string
	Owner            string
	VC               []string            // Verifiable Credentials
	CustomAttributes map[string][]string // Additional attributes like tags
}

// Matcher defines conditions under which a policy should apply. It includes lists of agents,
// clients, and issuers, as well as verifiable credentials. Boolean fields represent special
// agent or client types like public agents or authenticated agents, allowing for more granular
// control over the access decision process.
type Matcher struct {
	Agents             []string
	Clients            []string
	Issuers            []string
	VCs                []string
	PublicAgent        bool
	AuthenticatedAgent bool
	CreatorAgent       bool
	OwnerAgent         bool
	PublicClient       bool
	PublicIssuer       bool
}

// AccessControl links Access Control Resources (ACRs) to specific policies. It consists of
// a list of policies that dictate the access control logic for the associated resources.
type AccessControl struct {
	AppliedPolicies []Policy
}

// AuthorizationGraph defines the conditions for accessing a particular resource.
// It associates a resource with its relevant AccessControl configurations.
type AuthorizationGraph struct {
	Resource      string
	AccessControl []AccessControl
}

// Policy details the specific access rules and conditions. It defines what access modes are
// allowed or denied, and under which conditions (defined by matchers) these rules apply.
type Policy struct {
	AllowAccessMode []AccessMode
	Matchers        []Matcher
	DenyAccessModes []AccessMode
	AllOfMatchers   []Matcher
	AnyOfMatchers   []Matcher
	NoneOfMatchers  []Matcher
}

// AccessGrantGraph represents the actual access permission granted over a resource,
// detailing both the type of access granted and the context in which this grant is valid.
type AccessGrantGraph struct {
	Grant   string
	Context ContextGraph
}

// TODO:
// AccessControlResource serves as a bridge connecting resources to their specific
// AccessControls. This includes controls for both the resource and its member resources,
// supporting hierarchical access control structures.
type AccessControlResource struct {
	Resource             string
	AccessControls       []AccessControl
	MemberAccessControls []AccessControl // For hierarchical resources
}

// AccessGrant specifies the access modes that have been granted in a particular context.
// It provides a clear mapping of what access is allowed within the specified context.
type AccessGrant struct {
	AccessModes []string
	Context     ContextGraph
}

// AccessMode defines specific types of access that can be granted, such as Read or Write.
// This allows for easy expansion and customization of access types to suit specific needs.
type AccessMode string

const (
	ReadAccessMode   AccessMode = "Read"
	WriteAccessMode  AccessMode = "Write"
	DeleteAccessMode AccessMode = "Delete" // Example of a custom access mode
)

func main() {
	// Creating a ContextGraph instance
	context := ContextGraph{
		Target: "resourceX",
		Agent:  "Bob",
		Mode:   "Read",
		Client: "clientApplicationY",
		Issuer: "identityProviderZ",
	}

	// Creating an AuthorizationGraph instance
	authorization := AuthorizationGraph{
		Resource: "resourceX",
		AccessControl: []AccessControl{
			{
				AppliedPolicies: []Policy{
					{
						AllowAccessMode: []AccessMode{ReadAccessMode},
						Matchers: []Matcher{
							{
								Agents: []string{"Alice", "Bob"},
							},
						},
					},
				},
			},
		},
	}

	// Creating an AccessGrantGraph instance
	accessGrant := AccessGrantGraph{
		Grant:   "Read",
		Context: context,
	}

	// Print the structs to verify
	fmt.Printf("Context Graph: %+v\n", context)
	fmt.Printf("Authorization Graph: %+v\n", authorization)
	fmt.Printf("Access Grant Graph: %+v\n", accessGrant)

	contextGraphExample := ContextGraph{
		Target:  "resourceX",
		Agent:   "Bob",
		Mode:    "Read",
		Client:  "ClientApplicationY",
		Issuer:  "IdentityProviderZ",
		Creator: "Alice",
		Owner:   "Bob",
		VC:      []string{"credential1", "credential2"},
		CustomAttributes: map[string][]string{
			"tag": {"Music", "FavouriteRecord"},
		},
	}

	acrExample := AccessControlResource{
		Resource: "resourceX",
		AccessControls: []AccessControl{
			{
				AppliedPolicies: []Policy{
					{
						AllowAccessMode: []AccessMode{ReadAccessMode},
						Matchers: []Matcher{
							{
								Agents: []string{"Alice"},
							},
						},
					},
				},
			},
		},
		MemberAccessControls: []AccessControl{
			{
				AppliedPolicies: []Policy{
					{
						AllowAccessMode: []AccessMode{WriteAccessMode},
						Matchers: []Matcher{
							{
								Agents: []string{"Bob"},
							},
						},
					},
				},
			},
		},
	}

	accessControlExample := AccessControl{
		AppliedPolicies: []Policy{
			{
				AllowAccessMode: []AccessMode{ReadAccessMode},
				Matchers: []Matcher{
					{
						Agents: []string{"Alice", "Bob"},
					},
				},
			},
		},
	}

	policyAllowRead := Policy{
		AllowAccessMode: []AccessMode{ReadAccessMode},
		AllOfMatchers:   []Matcher{{Agents: []string{"Bob", "Alice"}}},
	}

	policyDenyWrite := Policy{
		DenyAccessModes: []AccessMode{WriteAccessMode},
		AnyOfMatchers:   []Matcher{{Agents: []string{"Bob", "Alice"}}},
	}

	complexPolicy := Policy{
		AllowAccessMode: []AccessMode{ReadAccessMode, WriteAccessMode},
		AnyOfMatchers:   []Matcher{{Agents: []string{"AgentA"}}},
		NoneOfMatchers:  []Matcher{{Agents: []string{"AgentB"}}},
	}

	matcherAgents := Matcher{
		Agents:     []string{"Alice"},
		OwnerAgent: true,
	}

	matcherIssuer := Matcher{
		Issuers: []string{"issuerB"},
	}

	matcherVC := Matcher{
		VCs: []string{"credentialB"},
	}

	complexMatcher := Matcher{
		Agents:  []string{"Alice", "Bob"},
		Issuers: []string{"IdentityProviderB"},
		VCs:     []string{"credentialA"},
	}

	accessGrantExample := AccessGrant{
		AccessModes: []string{string(ReadAccessMode), string(WriteAccessMode)},
		Context: ContextGraph{
			Agent:  "Alice",
			Target: "resourceX",
		},
	}

	extendedAccessGrant := AccessGrant{
		AccessModes: []string{string(ReadAccessMode), string(DeleteAccessMode)},
		Context: ContextGraph{
			Agent:  "Bob",
			Target: "resourceX",
		},
	}

	// Print Context Graph
	fmt.Printf("Context Graph: %+v\n", context)
	fmt.Printf("Context Graph Example: %+v\n", contextGraphExample)

	// Print Authorization Graph
	fmt.Printf("Authorization Graph: %+v\n", authorization)

	// Print Access Control Resource
	fmt.Printf("Access Control Resource Example: %+v\n", acrExample)

	// Print Access Control Example
	fmt.Printf("Access Control Example: %+v\n", accessControlExample)

	// Print Policy Examples
	fmt.Printf("Policy Allow Read: %+v\n", policyAllowRead)
	fmt.Printf("Policy Deny Write: %+v\n", policyDenyWrite)
	fmt.Printf("Complex Policy: %+v\n", complexPolicy)

	// Print Matcher Examples
	fmt.Printf("Matcher Agents: %+v\n", matcherAgents)
	fmt.Printf("Matcher Issuer: %+v\n", matcherIssuer)
	fmt.Printf("Matcher VC: %+v\n", matcherVC)
	fmt.Printf("Complex Matcher: %+v\n", complexMatcher)

	// Print Access Grant Graph
	fmt.Printf("Access Grant Graph: %+v\n", accessGrant)

	// Print Access Grant Examples
	fmt.Printf("Access Grant Example: %+v\n", accessGrantExample)
	fmt.Printf("Extended Access Grant: %+v\n", extendedAccessGrant)

}

func gatherEffectivePolicies(acr AccessControlResource, ancestorAcrs []AccessControlResource) []Policy {
	var effectivePolicies []Policy

	// Add policies from the primary ACR
	for _, ac := range acr.AccessControls {
		effectivePolicies = append(effectivePolicies, ac.AppliedPolicies...)
	}

	// Add policies from ancestor ACRs
	for _, ancestor := range ancestorAcrs {
		for _, ac := range ancestor.MemberAccessControls {
			effectivePolicies = append(effectivePolicies, ac.AppliedPolicies...)
		}
	}

	return effectivePolicies
}

func grantAccessModes(policies []Policy, context ContextGraph) []AccessMode {
	var allowedAccessModes, deniedAccessModes []AccessMode

	for _, policy := range policies {
		if isSatisfiedPolicy(policy, context) {
			allowedAccessModes = append(allowedAccessModes, policy.AllowAccessMode...)
			deniedAccessModes = append(deniedAccessModes, policy.DenyAccessModes...)
		}
	}

	// Deny overrules allow
	return resolveAccessModes(allowedAccessModes, deniedAccessModes)
}

func resolveAccessModes(allowed, denied []AccessMode) []AccessMode {
	finalModes := make(map[AccessMode]bool)
	for _, mode := range allowed {
		finalModes[mode] = true
	}
	for _, mode := range denied {
		delete(finalModes, mode)
	}

	var result []AccessMode
	for mode := range finalModes {
		result = append(result, mode)
	}

	return result
}

func isSatisfiedPolicy(policy Policy, context ContextGraph) bool {
	allOfSatisfied := len(policy.AllOfMatchers) == 0
	anyOfSatisfied := len(policy.AnyOfMatchers) == 0
	noneOfSatisfied := false

	for _, matcher := range policy.AllOfMatchers {
		if isSatisfiedMatcher(matcher, context) {
			allOfSatisfied = true
			break
		}
	}

	for _, matcher := range policy.AnyOfMatchers {
		if isSatisfiedMatcher(matcher, context) {
			anyOfSatisfied = true
			break
		}
	}

	for _, matcher := range policy.NoneOfMatchers {
		if isSatisfiedMatcher(matcher, context) {
			noneOfSatisfied = true
			break
		}
	}

	return allOfSatisfied && anyOfSatisfied && !noneOfSatisfied
}

func isSatisfiedMatcher(matcher Matcher, context ContextGraph) bool {
	agentMatch := len(matcher.Agents) == 0
	clientMatch := len(matcher.Clients) == 0
	issuerMatch := len(matcher.Issuers) == 0
	vcMatch := len(matcher.VCs) == 0

	for _, agent := range matcher.Agents {
		if agent == context.Agent {
			agentMatch = true
			break
		}
	}

	for _, client := range matcher.Clients {
		if client == context.Client {
			clientMatch = true
			break
		}
	}

	for _, issuer := range matcher.Issuers {
		if issuer == context.Issuer {
			issuerMatch = true
			break
		}
	}

	for _, vc := range matcher.VCs {
		for _, contextVc := range context.VC {
			if vc == contextVc {
				vcMatch = true
				break
			}
		}
	}

	// Add logic for PublicAgent, AuthenticatedAgent, etc., based on requirements
	// ...

	return agentMatch && clientMatch && issuerMatch && vcMatch
}
