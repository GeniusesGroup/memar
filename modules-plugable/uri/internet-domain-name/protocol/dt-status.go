/* For license and copyright information please see the LEGAL file in the code repository */

package domain_p

type Field_Status interface {
	Status() Status
}

// Status indicate UserDomain record status
type Status uint8

// UserDomain statuses
const (
// Status_ = Status(Status_FreeFlag << iota)
)
