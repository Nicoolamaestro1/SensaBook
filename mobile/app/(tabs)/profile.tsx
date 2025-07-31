import { View, Text } from 'react-native'
import React from 'react'

export default function Profile() {
  return (
    <View style={{ flex: 1, justifyContent: "center", alignItems: "center", backgroundColor: "#307A33FF" }}>
      <Text style={{ color: "white", fontSize: 32, fontWeight: "bold" }}>Profile</Text>
    </View>
  )
}