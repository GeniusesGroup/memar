/* For license and copyright information please see the LEGAL file in the code repository */

package domain_p

// UserDomain_AP is user domain accepted protocols
type UserDomain_AP uint8

const (
	UserDomain_AP_Unset UserDomain_AP = iota
	UserDomain_AP_Email
	UserDomain_AP_SMS
	UserDomain_AP_PhoneCall
)
