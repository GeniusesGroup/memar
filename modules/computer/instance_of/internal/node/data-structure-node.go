/* For license and copyright information please see the LEGAL file in the code repository */

package node

// NodeDataStructure ---Read locale description in nodeDataStructure---
type NodeDataStructure struct {
	ID              [32]byte // hash(AppID + ThingID)
	ThingID         [32]byte
	ReplicationID   uint8
	DataCenterID    [32]byte
	StorageCapacity uint64
	// Metric
}
