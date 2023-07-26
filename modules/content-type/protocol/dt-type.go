/* For license and copyright information please see the LEGAL file in the code repository */

package ctp

type Type uint16

const (
	Type_Unset Type = iota

	// Article use for many thing like NEWS, blog, education systems, features, ...
	Type_Article
	Type_BlogPost
	Type_NewsLetter

	Type_Book
	Type_Course
	Type_Tutorial

	Type_Music
	Type_Album
	Type_Concert
	Type_MusicVideo

	Type_Movie
	Type_Serial
	Type_SerialEpisode

	Type_Game
	Type_SportGame
)
