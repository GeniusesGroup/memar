/* For license and copyright information please see the LEGAL file in the code repository */

package graph_p

import (
	graph_p "memar/adt/graph/protocol"
	request_p "memar/process/request/protocol"

	thing_p "org/modules/identity/thing/protocol"
	label_p "org/modules/knowledge/label/protocol"
)

// Some usage example:
// - Task (123456) relate to Task (654321) by (Child Task) label
// - Task (369852) relate to Product (147852) by (QC) label
// - Product (toothbrush x) relate to Product (Toothpaste y) by (Complement) label
// - [law, User, label] >> ["VAT", "Thief User", "Law Suggester"] || ["VAT", "Omid", "Disagree"] ||
// - [Task, User, label] >> Task (123456) relate to User (Omid) by (Assigner) label
// - [User, User, label] >>  ["Omid", "Bill Gates", "KnownNames"] ||
// - [User, Org, label] >> ["Omid", "Persia", "Citizen"] ||

// DataModel indicate the domain record data fields.
//
// Save in on device node as PrimaryNode() but with PrimaryKey as sha3.256(PrimaryNode, SecondaryNode) in related GraphDataTypeID.
//   - One secondary key can exist to list all SecondaryNode for PrimaryNode.
//     But in some cases it isn't practical e.g. all relation to a city.
//   - On some requirements may need more secondary indexes e.g. all "act" relation for an actor to get all movies or vice versa
//
// But is it true to save these type of data as graph structure? Isn't it so simple to has dedicated media type?
// We think we must graph structure to store time sensitive data that a relation change over times.
// https://en.wikipedia.org/wiki/Graph_database
// https://stackoverflow.com/questions/43712490/time-based-graph-data-modeling
// https://www.researchgate.net/publication/324435978_Graph_based_Platform_for_Electricity_Market_Study_Education_and_Training
// https://github.com/milvus-io/milvus
type DataModel interface {
	// Edge indicate relation reason e.g. Complement, Substitute, ...
	graph_p.Graph[thing_p.UUID, thing_p.UUID, label_p.UUID]

	request_p.Field_RequestID
}

// TODO::: below model not work in huge data e.g. a user with millions of follower.
type Storage_DataModel interface {
	VertexID() thing_p.UUID
	Sides() []interface {
		Edge() label_p.UUID
		Vertex() thing_p.UUID
		request_p.Field_RequestID
	}
}

// OR>>

type Storage_DataModel_Edges interface {
	VertexID() thing_p.UUID
	Edges() []label_p.UUID
}

type Storage_DataModel_ByEdge interface {
	VertexID() thing_p.UUID
	Edge() label_p.UUID
	Sides() []interface {
		Vertex() thing_p.UUID
		request_p.Field_RequestID
	}
}
