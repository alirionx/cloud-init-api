<template>
  <div class="pagePartDiv">
    <div class="pagePartBar" @click="switch_component()">
      <div class="title">{{title}}</div>
      <div class="arrow " :class="{aUp: active, aDown: !active}"></div>
    </div>
    <div class="pagePartContentFrame" v-if="active">
      <form @submit.prevent="submit_form">
      
      <!------------------------------------------------------------->
      <div class="cloudConfigDiv">
        <div class="hl">General Parameters</div>
        
        <div class="formCard">
          <table class="formElm"><tr>
            <th>
              <span>Config Name:</span>
            </th>
            <td>
              <input type="text" required v-model="formData.name" placeholder="*" />
            </td>
          </tr></table>
          <table class="formElm"><tr>
            <th>
              <span>Instance Id:</span>
            </th>
            <td>
              <input type="text" required v-model="formData.meta_data.instance_id" placeholder="*" />
            </td>
          </tr></table>
          <table class="formElm"><tr>
            <th>
              <span>Hostname::</span>
            </th>
            <td>
              <input type="text" required v-model="formData.meta_data.local_hostname" placeholder="*" />
            </td>
          </tr></table>
        </div>

        <div class="formCard">
          <table class="formElm"><tr>
            <th>
              <span>Distro Name:</span>
            </th>
            <td>
              <input type="text" v-model="formData.meta_data.distro" placeholder="" />
            </td>
          </tr></table>
          <table class="formElm"><tr>
            <th>
              <span>Distro Version:</span>
            </th>
            <td>
              <input type="text" v-model="formData.meta_data.distro_version" placeholder="" />
            </td>
          </tr></table>
        </div>

      </div>
      
      <!------------------------------------------------------------->
      <div class="cloudConfigDiv">
        <div class="hl">Network Configuration</div>
        
        <div class="formCard">
          <table class="formElm"><tr>
            <th>
              <span>Source NIC Pattern:</span>
            </th>
            <td>
              <input type="text" required v-model="formData.network_config.src_nic_match" placeholder="*" />
            </td>
          </tr></table>
          <table class="formElm"><tr>
            <th>
              <span>Target NIC Name:</span>
            </th>
            <td>
              <input type="text" required v-model="formData.network_config.tgt_nic_name" placeholder="*" />
            </td>
          </tr></table>
          <table class="formElm"><tr>
            <th>
              <span>DHCP 4:</span>
            </th>
            <td>
              <input type="checkbox" v-model="formData.network_config.dhcp4" />
            </td>
          </tr></table>
        </div>

        <div class="formCard" v-if="!formData.network_config.dhcp4">
          <table class="formElm"><tr>
            <th>
              <span>IPv4 CIDRs:</span>
              <button 
                type="button" 
                class="inCellBtn" 
                @click="add_entry(formData.network_config.ip4_cidrs)">+</button>
            </th>
            <td>
              <div style="position:relative;" v-for="(cidr, idx) in formData.network_config.ip4_cidrs" :key="idx" >
                <button 
                  type="button" 
                  class="inCellBtn" 
                  @click="del_entry(formData.network_config.ip4_cidrs, idx)">-</button>
                <input 
                  type="text" 
                  v-model="formData.network_config.ip4_cidrs[idx]" 
                  placeholder="e.g. 192.168.0.10/24" />
              </div>
            </td>
          </tr></table>
          <table class="formElm"><tr>
            <th>
              <span>IPv4 Gateway:</span>
            </th>
            <td>
              <input type="text" v-model="formData.network_config.ip4_gw" placeholder="e.g. 192.168.0.1" />
            </td>
          </tr></table>
          <table class="formElm"><tr>
            <th>
              <span>Nameservers:</span>
              <button 
                type="button" 
                class="inCellBtn" 
                @click="add_entry(formData.network_config.nameservers)">+</button>
            </th>
            <td>
              <div style="position:relative;" v-for="(cidr, idx) in formData.network_config.nameservers" :key="idx" >
                <button 
                  type="button" 
                  class="inCellBtn" 
                  @click="del_entry(formData.network_config.nameservers, idx)">-</button>
                <input 
                  type="text" 
                  v-model="formData.network_config.nameservers[idx]" 
                  placeholder="e.g. 8.8.8.8" />
              </div>
            </td>
          </tr></table>
          <table class="formElm"><tr>
            <th>
              <span>Searches:</span>
              <button 
                type="button" 
                class="inCellBtn" 
                @click="add_entry(formData.network_config.searches)">+</button>
            </th>
            <td>
              <div style="position:relative;" v-for="(cidr, idx) in formData.network_config.searches" :key="idx" >
                <button 
                  type="button" 
                  class="inCellBtn" 
                  @click="del_entry(formData.network_config.searches, idx)">-</button>
                <input 
                  type="text" 
                  v-model="formData.network_config.searches[idx]" 
                  placeholder="e.g. homedom.local" />
              </div>
            </td>
          </tr></table>
        
        </div>
      </div>

      <!------------------------------------------------------------->
      <div class="cloudConfigDiv">
        <div class="hl">Users</div>
        <img src="@/assets/icon_useradd.png" class="userAddBtn" @click="add_user" />

        <div class="userSeparator" v-for="(user, idx) in formData.user_data.users" :key="idx">
          <div class="formCard">
            <table class="formElm"><tr>
              <th>
                <span>Username:</span>
              </th>
              <td>
                <input type="text" required v-model="formData.user_data.users[idx].name" placeholder="*" />
              </td>
            </tr></table>
            <table class="formElm"><tr>
              <th>
                <span>Password:</span>
              </th>
              <td>
                <input type="password" required v-model="formData.user_data.users[idx].passwd" placeholder="*" />
              </td>
            </tr></table>

            <table class="formElm"><tr>
              <th>
                <span>Lock Passwd:</span>
              </th>
              <td>
                <input type="checkbox" v-model="formData.user_data.users[idx].lock_passwd" />
              </td>
            </tr></table>

            <table class="formElm"><tr>
              <th>
                <span>Shell:</span>
              </th>
              <td>
                <select v-model="formData.user_data.users[idx].shell" >
                  <option value="/bin/sh">/bin/sh</option>
                  <option value="/bin/bash">/bin/bash</option>
                  <option value="/bin/zsh">/bin/zsh</option>
                </select>
              </td>
            </tr></table>

            <table class="formElm"><tr>
              <th>
                <span>Sudo Rules:</span>
              </th>
              <td>
                <input type="text" required v-model="formData.user_data.users[idx].sudo" placeholder="" />
              </td>
            </tr></table>

            <table class="formElm"><tr>
              <th>
                <span>Groups:</span>
                <button 
                  type="button" 
                  class="inCellBtn" 
                  @click="add_entry(formData.user_data.users[idx].groups)">+</button>
              </th>
              <td>
                <div style="position:relative;" v-for="(grp, idx2) in formData.user_data.users[idx].groups" :key="idx2" >
                  <button 
                    type="button" 
                    class="inCellBtn" 
                    @click="del_entry(formData.user_data.users[idx].groups, idx2)">-</button>
                  <input 
                    type="text" 
                    v-model="formData.user_data.users[idx].groups[idx2]" 
                    placeholder="e.g. sudo" />
                </div>
              </td>
            </tr></table>
          </div>

          <div class="formCard">
            <table class="formElm"><tr>
              <th>
                <span>SSH Password Auth:</span>
              </th>
              <td>
                <input type="checkbox" v-model="formData.user_data.users[idx].ssh_pwauth" />
              </td>
            </tr></table>
            <table class="formElm"><tr>
              <th>
                <span>Package Update:</span>
              </th>
              <td>
                <input type="checkbox" v-model="formData.user_data.users[idx].package_update" />
              </td>
            </tr></table>
            
            <table class="formElm"><tr>
              <th>
                <span>Packages:</span>
                <button 
                  type="button" 
                  class="inCellBtn" 
                  @click="add_entry(formData.user_data.users[idx].packages)">+</button>
              </th>
              <td>
                <div style="position:relative;" v-for="(grp, idx2) in formData.user_data.users[idx].packages" :key="idx2" >
                  <button 
                    type="button" 
                    class="inCellBtn" 
                    @click="del_entry(formData.user_data.users[idx].packages, idx2)">-</button>
                  <input 
                    type="text" 
                    v-model="formData.user_data.users[idx].packages[idx2]" 
                    placeholder="e.g. git" />
                </div>
              </td>
            </tr></table>

            <table class="formElm"><tr>
              <th>
                <span>SSH Public Key:</span>
              </th>
              <td>
                <textarea v-model="formData.user_data.users[idx].ssh_authorized_keys" placeholder="" >
                </textarea>
              </td>
            </tr></table>

          </div>
        </div>
      </div>
      
      <!------------------------------------------------------------->

      <div>
        <button type="submit">submit</button>
      </div>
         
      </form>
    </div>
  </div>
</template>

<script>
import { useMainStore } from '@/stores/mainStore'

export default {
  name: "Form",
  setup(){
    const store = useMainStore()
    return { store }
  }, 
  data(){
    return {
      id: "form",
      title: "CloudInit Iso Creation - Form",
      active: true,

      userModel:{
        name: null,
        passwd: null,
        // chpasswd: "{ expire: False }",
        lock_passwd: false,
        shell: "/bin/bash",
        sudo: "ALL=(ALL) NOPASSWD:ALL",
        groups: [ "sudo" ],
        ssh_pwauth: false,
        ssh_authorized_keys: null,
        package_update: false,
        packages: [],
        // package_upgrade: false
      },

      formData: {
        name: null,
        meta_data: {
          instance_id: null,
          local_hostname: null,
          distro: null,
          distro_version: null
        },
        user_data: {
          users: []
        },
        "network_config": {
          src_nic_match: "eth*",
          tgt_nic_name: "eth0",
          dhcp4: true,
          ip4_cidrs: [""],
          ip4_gw: null,
          nameservers: [],
          searches: []
        }
      }

    }
  },
  methods:{
    switch_component(){
      this.active = !this.active
    },
    add_entry(ary){
      if(ary[ary.length-1] == ""){
        return
      }
      ary.push("")
    },
    del_entry(ary, idx){
      ary.splice(idx, 1)
    }, 
    add_user(){
      console.log("new User")
      // let userItem = {...this.userModel}
      let userItem = JSON.parse(JSON.stringify(this.userModel))
      this.formData.user_data.users.push(userItem)

    },
    submit_form(){
      console.log(this.formData)
    }
  },
};
</script>

<style scoped>

.cloudConfigDiv{
  margin: 2px auto 12px auto;
  padding:16px;
  box-shadow: 0px 2px 3px #444;
  position: relative;
}
.cloudConfigDiv .hl{
  font-size: 16px;
  text-decoration: underline;
  font-weight: bold;
  color: #000;
  text-align: left;
  padding: 0 0 6px 0;
  margin-top: -4px;
}
.cloudConfigDiv .userAddBtn{
  height: 40px;
  cursor: pointer;
  border-radius: 4px;
  position: absolute;
  top:8px;
  right:10px;
  border: 1px solid rgba(0,0,0,0);
}
.cloudConfigDiv .userAddBtn:hover{
  border: 1px solid #333;
}

.formCard{
  width: 45%;
  min-width: 400px;
  max-width: 800px;
  /* border: 1px solid #aaa; */
  display: inline-block;
  text-align: left;
  margin-right: 45px;
  vertical-align: top;
}
.formCard:last-child{
  margin-right: 0px;
}
.formCard .formElm{
  width: 100%;
}
.formCard .formElm th{
  padding:6px;
  background-color: rgb(87, 109, 126);
  color: #fff;
  font-size: 14px;
  font-weight: bold;
  width:30%;
  position: relative;
  vertical-align: top;
}
.formCard .formElm td{
  width:auto;
  vertical-align: top;
}

.formCard .inCellBtn{
  position: absolute;
  right: 6px;
  top: 6px;
  font-weight: bold;
  cursor: pointer;
}

.formCard input[type=text], input[type=password], input[type=number]{
  margin: -1px 0 0 4px;
  padding: 8px 8px 9px 8px;
  width:96%;
  font-size: 15px;
  border: 1px solid #666;
  /* box-shadow: 0px 1px 2px #444; */
}
.formCard input[type=checkbox]{
  transform: scale(1.5);
  margin:10px 0 0 10px;
}

.formCard select{
  margin: 0 0 0 4px;
  padding: 8px 8px 9px 8px;
  width:50%;
  font-size: 15px;
  border: 1px solid #666;
  /* box-shadow: 0px 1px 2px #444; */
}

.formCard textarea{
  margin: 0 0 -6px 4px;
  padding: 4px;
  width:98%;
  font-size: 13px;
  border: 1px solid #666;
  min-height: 70px;
  resize: none;
  /* box-shadow: 0px 1px 2px #444; */
}

.userSeparator{
  border-bottom: 2px solid #444;
  margin-bottom: 8px;
  padding: 4px 0 12px 0;
}
.userSeparator:last-child{
  border-bottom: 0px;
  margin-bottom: 0px;
}



</style>