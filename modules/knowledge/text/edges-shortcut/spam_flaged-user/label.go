/* For license and copyright information please see the LEGAL file in the code repository */

package spam_flagged__user

// (user)-[:own]->(request)-><-[:spam]->(text)
//
// (text)-[:spam_flagged__user_by]->(user)
//
// (user)-[:spam_flagged__user_for]->(text)

// Policy (user):::
//
