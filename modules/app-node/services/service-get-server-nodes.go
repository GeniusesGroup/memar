/* For license and copyright information please see the LEGAL file in the code repository */

package services

import (
	"memar/net/srpc"
	"memar/protocol"
	"memar/service"
)

var getServerNodesService = service.Service{
	URN:                "domain/node.protocol.service; name=get-server-nodes",
	Domain:             DomainName,
	ID:                 639492616,
	IssueDate:          1595478242,
	ExpiryDate:         0,
	ExpireInFavorOfURN: "",
	ExpireInFavorOfID:  0,
	Status:             protocol.Software_PreAlpha,

	Authorization: authorization.Service{
		CRUD:     authorization.CRUDRead,
		UserType: protocol.UserType_All, // TODO::: ??
	},

	Detail: map[protocol.LanguageID]service.ServiceDetail{
		protocol.LanguageEnglish: {
			Name:        "Get Server Nodes",
			Description: `Returns all platforms nodes ID and connection details`,
			TAGS:        []string{},
		},
	},

	SRPCHandler: GetServerNodesSRPC,
}

// GetServerNodesSRPC is sRPC handler of GetServerNodes service.
func GetServerNodesSRPC(st protocol.Stream) {
	var res *getServerNodesRes
	res, err = getServerNodes(st)
	// Check if any error occur in bussiness logic
	if err != nil {
		return
	}

	st.OutcomePayload = make([]byte, srpc.MinLength+res.LenAsSyllab())
	res.ToSyllab(srpc.GetPayload(st.OutcomePayload))
}

type getServerNodesRes struct {
	nodes []NodeDetails
}

func getServerNodes(st protocol.Stream) (res *getServerNodesRes, err protocol.Error) {
	res = &getServerNodesRes{}
	res.nodes = App.Nodes.GetServerNodeDetails()
	return
}

func (res *getServerNodesRes) ToSyllab(payload []byte, stackIndex, heapIndex uint32) (freeHeapIndex uint32) {
	return
}

func (res *getServerNodesRes) LenAsSyllab() uint64 {
	return
}
