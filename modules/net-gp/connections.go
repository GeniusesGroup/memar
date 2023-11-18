/* For license and copyright information please see the LEGAL file in the code repository */

package gp

import (
	"strconv"
	"sync"
	"time"

	"memar/connection"
	"memar/protocol"
)

// Connections store pools of connection to retrieve in many ways
type Connections struct {
	mutex                      sync.Mutex
	poolByPeerAddr             map[Addr]*Connection
	poolByUserIDDelegateUserID map[[32]byte]*Connection
	poolByUserID               map[protocol.UserUUID][]*Connection
	poolByDomain               map[string]*Connection
	poolByBlackList            map[Addr]*Connection // key is PeerAddr
	shutdownSignal             chan struct{}

	connection.ConnectionsMetric
}

//libgo:impl memar/protocol.ObjectLifeCycle
func (c *Connections) Init() (err protocol.Error) {
	// TODO::: below numbers must calculate by hardware capacity!
	c.poolByPeerAddr = make(map[Addr]*Connection, 16384)
	c.poolByUserIDDelegateUserID = make(map[[32]byte]*Connection, 16384)
	c.poolByUserID = make(map[protocol.UserUUID][]*Connection, 16384)
	c.poolByDomain = make(map[string]*Connection, 16384)
	c.poolByBlackList = make(map[Addr]*Connection, 256)
	c.shutdownSignal = make(chan struct{})

	go c.connectionIdleTimeoutSaveAndFree()
	return
}
func (c *Connections) Reinit() (err protocol.Error) {
	return
}
func (c *Connections) Deinit() (err protocol.Error) {
	c.shutdownSignal <- struct{}{}

	// TODO::: log or dispatch start event? dispatch in app or internal listeners?
	// log.Info(&Package_MediaType, "ShutDown - Saving process begin ...\n"+
	// 	"Number of active connections:"+c.activeConnectionsNumber())

	for _, conn := range c.poolByUserIDDelegateUserID {
		go conn.Close()
	}

	// TODO::: log or dispatch end event? dispatch in app or internal listeners?
	// log.Info(&Package_MediaType, "ShutDown - Saving process end now")
	return
}

// GetConnectionByPeerAddr get a connection by peer GP from connections pool.
func (c *Connections) GetConnectionByPeerAddr(addr Addr) (conn *Connection, err protocol.Error) {
	conn = c.poolByPeerAddr[addr]
	if conn == nil {
		err = &connection.ErrNoConnection
	}
	return
}

// GetConnectionByUserIDDelegateUserID return the connection from pool or app storage.
// A connection can use just by single app node, so user can't use same connection to connect other node before close connection on usage node.
func (c *Connections) GetConnectionByUserIDDelegateUserID(userID, delegateUserID protocol.UserUUID) (conn *Connection, err protocol.Error) {
	conn = c.poolByUserIDDelegateUserID[c.userIDDelegateUserID(userID, delegateUserID)]
	if conn == nil {
		err = &connection.ErrNoConnection
	}
	return
}

// GetConnectionsByUserID get the connections by peer userID||domainID from connections pool.
func (c *Connections) GetConnectionsByUserID(userID protocol.UserUUID) (conn []*Connection, err protocol.Error) {
	conn = c.poolByUserID[userID]
	if conn == nil {
		err = &connection.ErrNoConnection
	}
	return
}

// GetConnectionByDomain return the connection from pool or app storage if any exist.
func (c *Connections) GetConnectionByDomain(domain string) (conn *Connection, err protocol.Error) {
	conn = c.poolByDomain[domain]
	if conn == nil {
		err = &connection.ErrNoConnection
	}
	return
}

// RegisterConnection register new connection in server connection pool
func (c *Connections) RegisterConnection(conn *Connection) (err protocol.Error) {
	c.mutex.Lock()
	defer c.mutex.Unlock()

	var userID = conn.UserID().UUID()
	c.poolByUserIDDelegateUserID[c.userIDDelegateUserID(userID, conn.DelegateUserID().UUID())] = conn
	if conn.Addr() != AddrNil {
		c.poolByPeerAddr[conn.Addr()] = conn
	}

	var connDomain = conn.DomainName()
	if connDomain != "" {
		c.poolByDomain[connDomain] = conn
	}

	if userID != protocol.UserUUID(AddrNil) {
		c.poolByUserID[userID] = append(c.poolByUserID[userID], conn)
	}

	if conn.UserID().Type() == protocol.UserType_Unset {
		c.ConnectionsMetric.GuestConnOpened()
	} else {
		c.ConnectionsMetric.ConnOpened()
	}
	return
}

// DeregisterConnection delete the given connection in connections pool
func (c *Connections) DeregisterConnection(conn *Connection) (err protocol.Error) {
	c.mutex.Lock()
	defer c.mutex.Unlock()
	err = c.deregisterConnection(conn)
	return
}

func (c *Connections) deregisterConnection(conn *Connection) (err protocol.Error) {
	var userID = conn.UserID().UUID()

	delete(c.poolByUserIDDelegateUserID, c.userIDDelegateUserID(userID, conn.DelegateUserID().UUID()))
	delete(c.poolByPeerAddr, conn.Addr())
	delete(c.poolByDomain, conn.DomainName())

	var userConnections = c.poolByUserID[userID]
	var userConnectionsLen = len(userConnections)
	for i := 0; i < userConnectionsLen; i++ {
		if userConnections[i].UserID().UUID() == userID {
			var newUserConnectionsLen = userConnectionsLen - 1
			// copy(userConnections[i:], userConnections[i+1:])
			// userConnections = userConnections[:newUserConnectionsLen]
			userConnections[i] = userConnections[newUserConnectionsLen]
			userConnections = userConnections[:newUserConnectionsLen]
			break
		}
	}
	c.poolByUserID[userID] = userConnections

	if conn.UserID().Type() == protocol.UserType_Unset {
		c.ConnectionsMetric.GuestConnClosed()
	} else {
		c.ConnectionsMetric.ConnClosed()
	}
	return
}

func (c *Connections) userIDDelegateUserID(userID, delegateUserID protocol.UserUUID) (userIDDelegateUserID [32]byte) {
	copy(userIDDelegateUserID[:], userID[:])
	copy(userIDDelegateUserID[16:], delegateUserID[:])
	return
}

func (c *Connections) connectionIdleTimeoutSaveAndFree() {
	var timer = time.NewTimer(ConnectionIdleTimeout)
	var timerTime time.Time
	for {
		select {
		case timerTime = <-timer.C:
			// TODO::: log or dispatch start event? dispatch in app or internal listeners?
			// log.Info(&Package_MediaType, "Cron - Idle connections timeout save and free process begin ...\n"+
			// 	"Number of active connections: "+c.activeConnectionsNumber())

			var timeNowMilli = timerTime.UnixMilli()

			c.mutex.Lock()
			defer c.mutex.Unlock()
			for _, conn := range c.poolByUserIDDelegateUserID {
				var lastUsage = conn.LastUsage()
				if lastUsage+ConnectionIdleTimeout < timeNowMilli {
					continue
				}

				c.deregisterConnection(conn)
				go conn.Close()
			}

			timer.Reset(ConnectionIdleTimeout)

			// TODO::: log or dispatch end event?
			// log.Info(&Package_MediaType, "Cron - Number of active connections after:"+c.activeConnectionsNumber()+
			// 	"\nIdle connections timeout save and free process end now")
		case <-c.shutdownSignal:
			return
		}
	}
}

func (c *Connections) activeConnectionsNumber() string {
	return strconv.FormatInt(int64(len(c.poolByUserIDDelegateUserID)), 10)
}
