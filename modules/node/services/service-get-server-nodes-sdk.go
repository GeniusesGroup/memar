/* For license and copyright information please see the LEGAL file in the code repository */

package services

// GetServerNodesRes is the response structure of GetServerNodes()
type GetServerNodesRes struct {
	nodes []NodeDetails
}

// GetServerNodes returns all platforms nodes ID and connection details
func GetServerNodes(s *App) (res *GetServerNodesRes, err error) {
	res = &GetServerNodesRes{}
	res.nodes = s.Nodes.GetServerNodeDetails()
	return
}
