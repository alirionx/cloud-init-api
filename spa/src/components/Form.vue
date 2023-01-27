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
        <img src="@/assets/icon_loadconfig.png" class="optBtn" @click="set_show_config_load" />
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
              <span>Hostname:</span>
            </th>
            <td>
              <input 
                type="text" 
                required 
                pattern="^[a-zA-Z0-9-]{4,16}$"
                v-model="formData.meta_data.local_hostname" 
                placeholder="*" />
            </td>
          </tr></table>
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

        <div class="formCard">
          <table class="formElm"><tr>
            <th>
              <span>Package Update:</span>
            </th>
            <td>
              <input type="checkbox" v-model="formData.user_data.package_update" />
            </td>
          </tr></table>

          <table class="formElm"><tr>
            <th>
              <span>Package Upgrade:</span>
            </th>
            <td>
              <input type="checkbox" v-model="formData.user_data.package_upgrade" />
            </td>
          </tr></table>
          
          <table class="formElm"><tr>
            <th>
              <span>Packages:</span>
              <button 
                type="button" 
                class="inCellBtn" 
                @click="add_entry(formData.user_data.packages)">+</button>
            </th>
            <td>
              <div style="position:relative;" v-for="(grp, idx2) in formData.user_data.packages" :key="idx2" >
                <button 
                  type="button" 
                  class="inCellBtn" 
                  @click="del_entry(formData.user_data.packages, idx2)">-</button>
                <input 
                  type="text" 
                  v-model="formData.user_data.packages[idx2]" 
                  placeholder="e.g. git" />
              </div>
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
                  pattern="^(?:[0-9]{1,3}\.){3}[0-9]{1,3}(\/([0-9]|[1-2][0-9]|3[0-2]))$"
                  placeholder="e.g. 192.168.0.10/24" />
              </div>
            </td>
          </tr></table>
          <table class="formElm"><tr>
            <th>
              <span>IPv4 Gateway:</span>
            </th>
            <td>
              <input 
                type="text" 
                v-model="formData.network_config.ip4_gw" 
                pattern="^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
                placeholder="e.g. 192.168.0.1" />
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
                  pattern="^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
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
        <img src="@/assets/icon_useradd.png" class="optBtn" @click="add_user" />

        <div class="userSeparator" v-for="(user, idx) in formData.user_data.users" :key="idx">
          <img src="@/assets/icon_userdel.png" class="optBtn del" @click="del_user(idx)" />
          <div class="formCard">
            <table class="formElm"><tr>
              <th>
                <span>Username:</span>
              </th>
              <td>
                <input 
                  type="text" 
                  required 
                  v-model="formData.user_data.users[idx].name" 
                  pattern="^[a-zA-Z0-9-]{2,16}$"
                  placeholder="*" />
              </td>
            </tr></table>
            <table class="formElm"><tr>
              <th>
                <span>Password:</span>
              </th>
              <td>
                <input 
                  type="password" 
                  required 
                  v-model="formData.user_data.users[idx].passwd" 
                  min="4"
                  placeholder="*" />
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
                <span>Sudo Rules:</span>
              </th>
              <td>
                <input type="text" required v-model="formData.user_data.users[idx].sudo" placeholder="" />
              </td>
            </tr></table>

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

      <div class="mainBtnFrame">
        <button type="submit">submit</button>
        <button type="button" @click="reset_form_data">reset</button>
      </div>
      </form>
    </div>
    <!------------------------------------------------------------->
    <div class="actionFormFrame" v-if="show_config_load">
      <div class="actionFormBox">
        <div class="hl">Load from existing Config</div>
        <div class="ipt_hl">Config Name</div>
        <select v-model="loaded_config">
          <option v-for="(item, idx) in store.isos" :value="idx">{{ item.name }}</option>
        </select>
        <div class="btnFrame">
          <button @click="load_config">load</button>
          <button @click="reset_show_config_load">close</button>
        </div>
      </div>
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
      active: false,
      show_config_load: false,
      loaded_config: null,
      userModel:{
        name: null,
        passwd: null,
        // chpasswd: "{ expire: False }",
        lock_passwd: false,
        shell: "/bin/bash",
        sudo: "ALL=(ALL) NOPASSWD:ALL",
        groups: [ "sudo" ],
        ssh_pwauth: false,
        ssh_authorized_keys: null
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
          package_update: false,
          package_upgrade: false,
          packages: [],
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
      },
      tmpFormData:{}

    }
  },
  methods:{
    switch_component(){
      this.active = !this.active
    },

    reset_form_data(){
      this.formData = JSON.parse(JSON.stringify(this.tmpFormData));
    },

    set_show_config_load(){
      this.show_config_load = true;
    },
    reset_show_config_load(){
      this.show_config_load = false;
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

    del_user(idx){
      this.formData.user_data.users.splice(idx, 1)
    }, 

    clear_empty_vals(obj){
      let tmp_obj = JSON.parse(JSON.stringify(obj));
      var isArray = tmp_obj instanceof Array;
      for (var k in tmp_obj){
        //syntax/kurzschreibweise hier verstehe ich nich... 
        if (tmp_obj[k]===null||tmp_obj[k]==="") isArray ? tmp_obj.splice(k,1) : delete tmp_obj[k]; 
        else if (typeof tmp_obj[k]=="object") this.clear_empty_vals(tmp_obj[k]);
      }
      return tmp_obj;
    },

    submit_form(){
      this.store.set_loader();
      let data = this.clear_empty_vals(this.formData)
      if(data.network_config.dhcp4){
        delete data.network_config["ip4_cidrs"];
        delete data.network_config["ip4_gw"];
      }
      let callback = ()=>{
        this.store.reset_loader()
        this.reset_form_data()
      }
      this.store.create_iso(data, callback) 
    },
    load_config(){
      if(this.loaded_config === null) return
      // console.log(this.store.isos[this.loaded_config])
      console.log( JSON.parse(JSON.stringify(this.store.isos[this.loaded_config].class_config_data)) )
      this.formData = JSON.parse(
        JSON.stringify(this.store.isos[this.loaded_config].class_config_data)
      );
      this.reset_show_config_load()
    }
  },
  mounted: function(){
    this.tmpFormData = JSON.parse(JSON.stringify(this.formData));
  }
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
  padding: 0 0 8px 0;
  margin-top: -4px;
}
.cloudConfigDiv .optBtn{
  height: 34px;
  cursor: pointer;
  border-radius: 4px;
  position: absolute;
  top:8px;
  right:18px;
  
}
.cloudConfigDiv .optBtn:hover{
  box-shadow: 1px 1px 2px #444;
}
.cloudConfigDiv .del{
  height: 28px;
  right:4px;
  top:10px;
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
  padding:4px 4px 4px 6px;
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
  right: 5px;
  top: 5px;
  font-weight: bold;
  cursor: pointer;
}

.formCard input[type=text], input[type=password], input[type=number]{
  margin: -1px 0 0 4px;
  padding: 5px 5px 8px 5px;
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
  margin-top: 12px;
  padding: 14px 0 2px 0;
  border-top: 2px solid #444;
  position:relative;
}

.mainBtnFrame{
  padding:4px;
  text-align: center;
}
.mainBtnFrame button{
  min-width: 120px;
  padding: 6px 12px 6px 12px;
  margin: 0px 10px 0px 10px;
  border-radius: 4px;
  text-align: center;
  background-color: rgb(62, 79, 93);
  color:#fff;
  font-size: 14px;
  font-weight: bold;
  cursor: pointer;
  border: none;
}
.mainBtnFrame button:hover{
  box-shadow: 1px 1px 2px #444;
}




</style>