import React from 'react';

const Dashboard = () => {
    return (
        <div className="dashboard-page mt-5 mb-5">
            <div className="container bg-white p-5">
                <h2 className="text-center"><b>Dashboard</b></h2>
                <div className="dashboard-content text-center">
                <iframe src="http://localhost:5601/app/dashboards#/view/a7e6236c-ff05-41dd-b1a5-870c788b0cc2?embed=true&_g=(refreshInterval:(pause:!t,value:60000),time:(from:now-1y%2Fd,to:now))&_a=()&hide-filter-bar=true" height="850" width="1000"></iframe>
                
                               </div>
            </div>
        </div>
    );
};

export default Dashboard;
