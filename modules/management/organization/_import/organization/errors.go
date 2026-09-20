/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	er "libgo/error"
	"libgo/protocol"
)

const domainEnglish = "Sabz.City"
const domainPersian = "شهرسبز"

// Errors
var (
	ErrOrgNameRegistered = er.New("urn:giti:sabz.city:error:org-name-registered").SetDetail(protocol.LanguageEnglish, domainEnglish, "Org Name Registered",
		"Given organization name to register new organization or update exiting organization already registered",
		"",
		"").Save()

	ErrOrgDomainRegistered = er.New("urn:giti:sabz.city:error:org-domain-registered").SetDetail(protocol.LanguageEnglish, domainEnglish, "Org Domain Registered",
		"Given organization domain to register new organization or update exiting organization already registered",
		"",
		"").Save()
)
