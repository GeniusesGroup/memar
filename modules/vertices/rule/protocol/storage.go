/* For license and copyright information please see the LEGAL file in the code repository */

package rule_p

// Provide a service to get rules by specific FieldID AND/OR FieldValue with specific label.
// e.g. find all discount rules that match for user with `123456` ID.
// It will need some strong cache system.
// e.g. each user see products page need to know about discount that compute by many rules match like location or labels!
