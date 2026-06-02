/* For license and copyright information please see the LEGAL file in the code repository */

package spam_checked

// (---)-[:spam_checker]->(rule)-[:checked]->(text)
//
// (text)-[:spam_checked_by]->(rule)
//
// (rule)-[:spam_checked_for]->(text)

// Policy (rule):::
// This rule MAY labeled any text that checked with its rules as `spam`
