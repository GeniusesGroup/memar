/* For license and copyright information please see the LEGAL file in the code repository */

package acp

import (
	"memar/protocol"

	aap "org/modules/app-audit/protocol"
	cp "org/modules/computer/protocol"
	cpkp "org/modules/cryptography-public_key/protocol"
	up "org/modules/user/protocol"
)

// Connection or App2AppConnection indicate how connection create and save in time series data.
// Each user pair with delegate-user has a chain that primary key is UserID+DelegateUserID
type Connection interface {
	ConnectionID() ConnectionUUID
	UserID() up.UserUUID
	DelegateUserID() up.UserUUID // Persons can delegate to things(as a user type)
	ComputerID() cp.ComputerUUID

	/* Connection data */
	MTU() int
	Weight() protocol.Weight

	/* Peer data */
	Addr() [16]byte
	// AddrType() protocol.NetworkLink_NextHeaderID

	/* Security data */
	// AccessControl() AccessControl
	PublicKey() cpkp.PublicKeyUUID
	CipherSuite() CipherSuite

	// ClientType() string // persiaos, web, android, ios, ...
	// Geo()                // location of user or post

	aap.AuditRequest
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
