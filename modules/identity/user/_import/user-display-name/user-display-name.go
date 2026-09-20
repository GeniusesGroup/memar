/* For license and copyright information please see the LEGAL file in the code repository */

package uds

import "libgo/protocol"

var userDisplayNameStructure = ds.DataStructure{
	URN:             "urn:giti:sabz.city:data-structure:user-display-name",
	ID:              8813670099917390348,
	IssueDate:       1599020151,
	ExpiryDate:      0,
	ExpireInFavorOf: "",
	Status:          protocol.Software_PreAlpha,
	Structure:       UserDisplayName{},

	Name: map[protocol.LanguageID]string{
		protocol.LanguageEnglish: "User Display Name",
	},
	Description: map[protocol.LanguageID]string{
		protocol.LanguageEnglish: "store user locale display name as replace for old fashion as first and family name to show or print in any pages",
	},
	TAGS: []string{
		"",
	},
}

// UserDisplayName ---Read locale description in userDisplayNameStructure---
type UserDisplayName struct {
	RequestID   [16]byte // user-request domain
	UserID      [16]byte `index-hash:"ObjectID"`
	DisplayName string   `index-text:"UserID"` // It is not unique and not replace of user ID. Just use to find user by desire name.
}
