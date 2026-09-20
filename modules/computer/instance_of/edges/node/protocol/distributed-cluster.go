/* For license and copyright information please see the LEGAL file in the code repository */

package node_p

import (
	datatype_p "memar/computer/datatype/protocol"
	error_p "memar/process/error/protocol"
	record_p "memar/storage/record/protocol"
)

// CLU is default global protocol.Cluster like window global variable in browsers.
// You must assign to it by any object implement protocol.Cluster on your main.go file. Suggestion:
// protocol.STG = &esteghrar.Cluster
var CLU Cluster

// Cluster store application nodes data and ready to return in many ways.
type Cluster interface {
	LocalNode() DataModel
	ReplicatedLocalNode() []DataModel

	GetReplicatedNodes(node DataModel) []DataModel
	GetNodeByID(nodeID UUID) DataModel
	GetNodeByStorage(dataTypeID datatype_p.ID, uuid record_p.UUID) (node DataModel, err error_p.Error)
}
