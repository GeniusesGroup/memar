/* For license and copyright information please see the LEGAL file in the code repository */

package cp

import (
	"memar/protocol"
)

type ApplicationNode interface {
	Type() NodeType
	ID() NodeID                    // as InstanceID
	DataCenterID() protocol.UserID // orgID
	ThingID() protocol.UserID
	ReplicationID() uint8
	StorageCapacity() uint64 // In bytes, Max 16EB(Exabyte) that more enough for one node capacity. 0 means service only node.
	Conn() protocol.Socket
	Status() protocol.ApplicationStatus
	Stats()
}

type NodeID UUID

type NodeType uint8

const (
	Node_Unset NodeType = iota
	Node_LocalNode
	Node_Cloud
	Node_Edge
	Node_GUI
)
