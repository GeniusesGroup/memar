/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// Connection or App2AppConnection indicate how connection create and save in time series data.
// Each user pair with delegate-user has a chain that primary key is UserID+DelegateUserID
type Connection interface {
	/* Connection data */
	MTU() int
	Status() protocol.NetworkStatus // return last connection state
	Weight() protocol.Weight

	/* Peer data */
	Addr() [16]byte
	AddrType() protocol.NetworkLink_NextHeaderID
	DomainName() string // if exist
	UserID() protocol.UserID
	DelegateUserID() protocol.UserID // Persons can delegate to things(as a user type)

	/* Security data */
	// AccessControl() AccessControl
	Cipher() protocol.Cipher
}

// ConnectionMetrics
type ConnectionMetrics interface {
	LastUsage() protocol.Time            // Last use of the connection
	MaxBandwidth() uint64                // Byte/Second and Connection can limit to a fixed number
	BytesSent() uint64                   // Counts the bytes of packets sent
	PacketsSent() uint64                 // Counts sent packets
	BytesReceived() uint64               // Counts the bytes of packets receive
	PacketsReceived() uint64             // Counts received packets
	FailedPacketsReceived() uint64       // Counts failed packets receive for firewalling server from some attack types
	NotRequestedPacketsReceived() uint64 // Counts not requested packets received for firewalling server from some attack types
	SucceedStreamCount() uint64          // Count successful request
	FailedStreamCount() uint64           // Count failed services call e.g. data validation failed, ...

	StreamSucceed()
	StreamFailed()
	PacketReceived(packetLength uint64)
	PacketSent(packetLength uint64)
}
