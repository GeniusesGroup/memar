/* For license and copyright information please see the LEGAL file in the code repository */

package services

// Details :
type Details struct {
	Name           string
	Type           string
	Picture        string
	ProducerOrg    string
	Guarantee      uint8 // In month
	Warranty       uint8 // In month
}

// Package :
type Package struct {
	Number string
	Mass   string
	Shape  string
}
// ThingsDetails :
type ThingsDetails struct {
	Name           string
	Type           string // Use for internal method. e.g. Lamp have 4 method! On/Off/Contrast/Color
	Picture        string
	BandwidthUsage uint // Approximately bandwidth needed
	ProducerOrg    string
	Guarantee      uint8 // In month
	Warranty       uint8 // In month
}