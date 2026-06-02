/* For license and copyright information please see the LEGAL file in the code repository */

package spam_flagged__rule

// (---)-[:spam_checker]->(rule)-[:own]->(request)-><-[:spam]->(text)
//
// (text)-[:spam_flagged__rule_by]->(rule)
//
// (rule)-[:spam_flagged__rule_for]->(text)

// Policy (rule):::
//
