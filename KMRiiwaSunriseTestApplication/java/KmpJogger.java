package kmr.test;


// RoboticsAPI
import com.kuka.jogging.provider.api.common.ICartesianJoggingSupport;
import com.kuka.roboticsAPI.deviceModel.kmp.SunriseOmniMoveMobilePlatform;

// Java Util
import java.util.TimerTask;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;


public class KmpJogger
{
  private long JOG_UPDATE_PERIOD = 50L;

  public ScheduledExecutorService _executor;

  private ICartesianJoggingSupport _joggableDevice;
  
  private double[] _velocities;
  

  
  public KmpJogger( ICartesianJoggingSupport joggableDevice, long updateperiod) {
	this._velocities = new double[3];
    this._joggableDevice = joggableDevice;
    this.JOG_UPDATE_PERIOD = updateperiod;
  }

  public KmpJogger( ICartesianJoggingSupport joggableDevice) {
	this._velocities = new double[3];
    this._joggableDevice = joggableDevice;
  }
  
  public class JogTimerTask
    extends TimerTask
  {
    public JogTimerTask() {}

    
    public void run() {
        
        if (KmpJogger.this._joggableDevice instanceof SunriseOmniMoveMobilePlatform && !((SunriseOmniMoveMobilePlatform)KmpJogger.this._joggableDevice).isReadyToMove()){
        	KmpJogger.this._executor.shutdown();
        }
        KmpJogger.this._joggableDevice.jog(KmpJogger.this._velocities);
           
    }
  }


  public void stopDevice() {
	    for (int i = 0; i < this._velocities.length; i++){
	      this._velocities[i] = 0.0D;
	    }

	    if(((SunriseOmniMoveMobilePlatform)KmpJogger.this._joggableDevice).isReadyToMove()){
		    this._joggableDevice.jog(this._velocities);
	    }
  }
  
  
  public void startJoggingExecution() {
    if (this._executor  ==null|| this._executor.isShutdown())
    {
      this._executor = Executors.newScheduledThreadPool(2);
    }
    this._executor.scheduleAtFixedRate(new JogTimerTask(), 
        0L, 
        this.JOG_UPDATE_PERIOD, 
        TimeUnit.MILLISECONDS);
    System.out.println("KMPjogger started");
  }


  public void killJoggingExecution(boolean ismoving) {
	  System.out.println("Stop KMPjogger");
	  if (this._executor != null) {
      try{
    	  this._executor.shutdown();
      }catch(Exception e){
    	  System.out.println("Could not stop executor in KMPjogger");
      }
    } 
	if(ismoving){
		stopDevice();
	}
  }
  
  
  public void updateVelocities(double[] vel) {
	  this._velocities = vel;

  }


  

	  
  
  
}