/* For license and copyright information please see the LEGAL file in the code repository */

package services

import (
	"memar/process/service"
	"memar/protocol"
)

// GetNodeDetailsService store details about GetNodeDetails service
var GetNodeDetailsService = service.Service{
	URN:                "domain/node.protocol.service; name=get-node-details",
	Domain:             DomainName,
	ID:                 2549172775244598073,
	IssueDate:          1596950889,
	ExpiryDate:         0,
	ExpireInFavorOfURN: "",
	ExpireInFavorOfID:  0,
	Status:             protocol.Software_PreAlpha,

	Authorization: authorization.Service{
		CRUD:     operation_p.ActionType_Read,
		UserType: user_p.Type_App,
	},

	Detail: map[protocol.LanguageID]service.ServiceDetail{
		protocol.LanguageEnglish: {
			Name:        "GetNodeDetails",
			Description: "Get node details that request receive",
			TAGS:        []string{},
		},
	},

	SRPCHandler: GetNodeDetailsSRPC,
}

// GetNodeDetailsSRPC is sRPC handler of GetNodeDetails service.
func GetNodeDetailsSRPC(st protocol.Stream) {
	if st.Connection.UserID != protocol.OS.AppManifest().AppUUID() {
		// TODO::: Attack??
		err = authorization.ErrUserNotAllow
		return
	}

	var res *Node
	res, err = GetNodeDetails(st)
	// Check if any error occur in business logic
	if err != nil {
		return
	}

	st.OutcomePayload = res.ToSyllab()
}

// GetNodeDetails returns local node details or related error!
func GetNodeDetails(st protocol.Stream) (res *Node, err error_p.Error) {
	res, err = Cluster.GetLocalNodeDetail()
	return
}

// GetServerNodeDetails returns all platform nodes details.
func (n *Nodes) GetServerNodeDetails() (nd []NodeDetails) {
	return n.nodesDetails
}

type getServerNodeDetailsRes struct {
	nodes []NodeDetails
}

func getServerNodeDetails(conn *Connection) (res *getServerNodeDetailsRes, err error_p.Error) {
	// Make new request-response streams
	var st *Stream
	st, err = conn.MakeOutcomeStream(0)
	if err != nil {
		return
	}

	// Set GetServerNodes ServiceID
	st.Service = &Service{ID: 639492616}

	err = SrpcOutcomeRequestHandler(st)
	if err != nil {
		return
	}

	err = res.FromSyllab(st.OutcomePayload)
	return
}

func (res *getServerNodeDetailsRes) FromSyllab(payload []byte, stackIndex uint32) {
	// TODO:::
	return nil
}

func (n *Node) getNodeDetails(node protocol.ApplicationNode) (err error_p.Error) {
	// Check if desire node is not a ganjine node!
	if node.Conn == nil {
		// err =
		return
	}

	// Make new request-response streams
	var st protocol.Stream
	st, err = node.Conn.OutcomeStream(&GetNodeDetailsService)
	if err != nil {
		return
	}

	err = srpc.OutcomeRequestHandler(st)
	if err != nil {
		return
	}

	n.FromSyllab(st.IncomePayload[4:])
	return err
}

// FromSyllab decode from buf to req
// Due to this service just use internally, It skip check buf size syllab rule! Panic occur if bad request received!
func (n *Node) FromSyllab(payload []byte, stackIndex uint32) {
	return
}

// ToSyllab encode req to buf
func (n *Node) ToSyllab(payload []byte, stackIndex, heapIndex uint32) (freeHeapIndex uint32) {
	return
}
