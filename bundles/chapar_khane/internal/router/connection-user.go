/* For license and copyright information please see the LEGAL file in the code repository */

package chaparkhane

import (
	"memar/net/connection"
	"memar/protocol"
)

// UserConnection can use by any type users
type UserConnection struct {
	/* Connection data */
	ID           [32]byte
	UserGPID     uint32 // Part of GP that lease by OS delegate of a user!
	Status       uint8  // States locate in this file.
	Weight       uint8  // 16 queue for priority weight of the connections exist.
	MaxBandwidth uint64 // Peer must respect this, otherwise connection will terminate and User go to black list!

	/* Peer data */
	Path            []byte // Chapar switch spec
	ReversePath     []byte // Chapar switch spec
	AlternativePath [][]byte
	ThingID         [16]byte
	UserID          [16]byte // Can't change after first set. 0 for Guest!
	UserType        uint8    // 0:Guest, 1:Registered 2:Person, 3:Org, 4:App, ...

	/* Security data */
	Cipher protocol.Cipher // Selected cipher algorithms https://en.wikipedia.org/wiki/Cipher_suite

	connection.Metric
}
