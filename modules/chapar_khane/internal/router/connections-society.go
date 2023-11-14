/* For license and copyright information please see the LEGAL file in the code repository */

package chaparkhane

import (
	"hash/crc32"

	"memar/net/chapar"
	"memar/crypto"
)

// societyConnections store pools of connection to retrieve in many ways!
type societyConnections struct {
	old              *societyConnections // use just in expanding
	pathsPool        [254][]*routerConnection
	SocietiesPoolLen uint32
	SocietiesPool    []societyPool
}

type societyPool struct {
	SocietyID uint32
	FreeID    uint8
	RouterID  [8]uint32
	Conn      [8]*routerConnection
}

func (sc *societyConnections) init() {
	// TotalHop = 1 or One hop frame use just in p2p networks and not pass here!!
	// TotalHop = 2 or Two hop implement by just one Chapar switch device!
	sc.pathsPool[0] = make([]*routerConnection, 256)
	// TotalHop > 2 or More than two hop implement by more than one Chapar switch device!
	var i uint8
	for i = 1; i < 255; i++ {
		sc.pathsPool[i] = make([]*routerConnection, 2048)
	}

	// TODO::: use existing society number instead of below 1024 number
	sc.SocietiesPool = make([]societyPool, 1024)
	sc.SocietiesPoolLen = 1024
}

func (sc *societyConnections) expandPathPool(hopNum uint8) (newPoolLen uint32) {
	var poolLen uint32 = uint32(len(sc.pathsPool[hopNum]))
	newPoolLen = poolLen * 2

	var new = make([]*routerConnection, newPoolLen)

	// Copy old paths
	var existingConn *routerConnection
	var loc uint32
	var i uint32
	for i = 0; i < poolLen; i++ {
		existingConn = sc.pathsPool[hopNum][i]
		if existingConn != nil {
			loc = crc32.ChecksumIEEE(existingConn.Path) % newPoolLen
			new[loc] = existingConn
		}
	}
	sc.pathsPool[hopNum] = new

	return
}

func (sc *societyConnections) expandSocietiesPool() {
	var newPoolLen uint32 = sc.SocietiesPoolLen * 2
	var new = make([]societyPool, newPoolLen)

	// Copy old Societies
	var sp societyPool
	var loc uint32
	var i uint32
	for i = 0; i < sc.SocietiesPoolLen; i++ {
		sp = sc.SocietiesPool[i]
		if sp.Conn[0] != nil {
			loc = sp.SocietyID % newPoolLen
			new[loc] = sp
		}
	}

	sc.SocietiesPool = new
	sc.SocietiesPoolLen = newPoolLen
}

// registerNewPath use to register or overwrite a path in the related pool!
func (sc *societyConnections) registerNewPath(conn *routerConnection, path []byte) {
	var pathLen uint8 = uint8(len(conn.Path))
	var poolLen uint32 = uint32(len(sc.pathsPool[pathLen]))
	var loc = crc32.ChecksumIEEE(conn.Path) % poolLen

	// Check collision!!
	var existingConn = sc.pathsPool[pathLen][loc]
	if existingConn != nil && existingConn.RouterID != conn.RouterID {
		poolLen = sc.expandPathPool(pathLen)
		loc = crc32.ChecksumIEEE(conn.Path) % poolLen
	}

	sc.pathsPool[pathLen][loc] = conn
}

// registerNewRouter use to register or overwrite a router in the related pool!
func (sc *societyConnections) registerNewRouter(conn *routerConnection) {
	var sp = sc.GetSocietyPool(conn.SocietyID)
	if sp != nil {
		if sp.SocietyID == conn.SocietyID {
			for i := 0; i < 8; i++ {
				// Check for existing connection
				if sp.RouterID[i] == conn.RouterID {
					sp.Conn[i].AlternativePath = append(sp.Conn[i].AlternativePath, conn.Path)
					sc.registerNewPath(sp.Conn[i], conn.Path)
				} else if sp.RouterID[i] == 0 {
					sp.FreeID++
					sp.RouterID[i] = conn.RouterID
					sp.Conn[i] = conn
					return
				}
			}
		} else {
			// Collision occurred!!
			sc.expandSocietiesPool()
			sc.registerNewRouter(conn)
		}
	} else {
		var sp = societyPool{
			SocietyID: conn.SocietyID,
			FreeID:    1,
			RouterID:  [8]uint32{conn.RouterID, 0, 0, 0, 0, 0, 0, 0},
			Conn:      [8]*routerConnection{conn, nil, nil, nil, nil, nil, nil, nil},
		}
		var societyLoc = conn.SocietyID % sc.SocietiesPoolLen
		sc.SocietiesPool[societyLoc] = sp
	}
}

// MakeNewSocietyConnectionReq is the request structure of MakeNewSocietyConnection()
type MakeNewSocietyConnectionReq struct {
	SocietyID    uint32
	RouterID     uint32
	Path         []byte
	MaxBandwidth uint64
	Signature    [256]byte
}

// MakeNewSocietyConnection use to make new connection!
func (sc *societyConnections) MakeNewSocietyConnection(req *MakeNewSocietyConnectionReq) {
	// TODO::: Check signature first!

	var conn = routerConnection{
		RouterID:     req.RouterID,
		Path:         req.Path,
		ReversePath:  chapar.ReversePath(req.Path),
		Status:       routerConnectionState_Open,
		MaxBandwidth: req.MaxBandwidth,
		Cipher:       crypto.NewGCM(crypto.NewAES256([32]byte{})),
	}
	sc.RegisterConnection(&conn)
}

// RegisterConnection use to register new connection in server societyConnections pool!!
func (sc *societyConnections) RegisterConnection(conn *routerConnection) {
	sc.registerNewPath(conn, conn.Path)
	sc.registerNewRouter(conn)
}

// GetConnectionByPath use to get a connection by peer GP from societyConnections pool!!
func (sc *societyConnections) GetConnectionByPath(path []byte) (conn *routerConnection) {
	var pathLen = len(path)
	var poolLen uint32 = uint32(len(sc.pathsPool[pathLen]))
	var loc = crc32.ChecksumIEEE(path) % poolLen

	conn = sc.pathsPool[pathLen][loc]
	return
}

// GetSocietyPool use to get a pool by given society ID from societyConnections pool!!
func (sc *societyConnections) GetSocietyPool(societyID uint32) (sp *societyPool) {
	var societyLoc = societyID % sc.SocietiesPoolLen
	sp = &sc.SocietiesPool[societyLoc]
	return
}

// GetConnectionBySocietyID use to get a connection by given society ID from societyConnections pool!!
func (sc *societyConnections) GetConnectionBySocietyID(societyID uint32) (conn *routerConnection) {
	var societyLoc = societyID % sc.SocietiesPoolLen
	conn = sc.SocietiesPool[societyLoc].Conn[0]

	// check if connection is in not ready status

	return
}

// CloseConnection use to un-register existing connection in societyConnections pool!!
func (sc *societyConnections) CloseConnection(conn *routerConnection) {
	// TODO::: Check GC performance : delete connection vs just reset it and send it to pool of unused connection!!
	var pathLen = len(conn.Path)
	var poolLen uint32 = uint32(len(sc.pathsPool[pathLen]))
	var loc = crc32.ChecksumIEEE(conn.Path) % poolLen
	var societyLoc = conn.SocietyID % sc.SocietiesPoolLen

	sc.pathsPool[pathLen][loc] = nil

	var i uint8
	var f = sc.SocietiesPool[societyLoc].FreeID
	var sp = sc.SocietiesPool[societyLoc]
	for ; i < f; i++ {
		if sp.RouterID[i] == conn.RouterID {
			sp.RouterID[i] = 0
			sp.Conn[i] = nil
			break
		}
	}
}
