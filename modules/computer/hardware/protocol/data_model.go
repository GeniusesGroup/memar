/* For license and copyright information please see the LEGAL file in the code repository */

package computer_p

import (
	org_p "org/modules/identity/org/protocol"
	thing_p "org/modules/identity/thing/protocol"
)

type ApplicationNode interface {
	Field_ComputerID
	Type() NodeType
	DataCenterID() org_p.OrgUUID
	thing_p.Field_ThingID
	StorageCapacity() uint64 // In bytes, Max 16EB(Exabyte) that more enough for one node capacity. 0 means service only node.
	// Conn() protocol.Socket
	Stats()
}

type NodeType uint8

const (
	Node_Unset NodeType = iota
	Node_LocalNode
	Node_Cloud
	Node_Edge
	Node_GUI
)
